using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using Mono.Cecil;

internal static class UnityApiMetadata
{
    private static int Main(string[] args)
    {
        if (args.Length < 2)
        {
            Console.Error.WriteLine(
                "usage: UnityApiMetadata <assembly> <query> [reference-directory ...]");
            return 2;
        }

        var query = NormalizeName(args[1]);
        var resolver = new DefaultAssemblyResolver();
        AddSearchDirectory(resolver, Path.GetDirectoryName(args[0]));
        for (var index = 2; index < args.Length; index++)
            AddSearchTree(resolver, args[index]);
        var assembly = AssemblyDefinition.ReadAssembly(
            args[0],
            new ReaderParameters
            {
                AssemblyResolver = resolver,
                ReadingMode = ReadingMode.Deferred
            });
        var count = 0;
        foreach (var type in AllTypes(assembly.MainModule.Types))
        {
            if (!IsPublic(type))
                continue;

            var typeName = FriendlyDeclaringType(type);
            if (Matches(query, typeName, type.Name))
            {
                Emit("type", assembly.Name.Name, typeName, Visibility(type) + " " + TypeKind(type)
                    + " " + typeName, type.Namespace, type, null);
                count++;
            }

            foreach (var method in type.Methods)
            {
                if (!IsPublic(method) || method.IsGetter || method.IsSetter
                    || method.IsAddOn || method.IsRemoveOn)
                    continue;
                var fqn = typeName + "." + method.Name + GenericParameters(method.GenericParameters);
                var signature = Visibility(method) + (method.IsStatic ? " static " : " ")
                    + FriendlyType(method.ReturnType) + " " + fqn + "("
                    + string.Join(", ", method.Parameters.Select(FormatParameter)) + ")";
                if (!Matches(query, fqn, signature))
                    continue;
                Emit("method", assembly.Name.Name, fqn, signature, type.Namespace, method, type);
                count++;
            }

            foreach (var property in type.Properties)
            {
                var accessor = property.GetMethod ?? property.SetMethod;
                if (accessor == null || !IsPublic(accessor))
                    continue;
                var fqn = typeName + "." + property.Name;
                var indexer = property.HasParameters
                    ? "[" + string.Join(", ", property.Parameters.Select(FormatParameter)) + "]"
                    : string.Empty;
                var signature = Visibility(accessor) + (accessor.IsStatic ? " static " : " ")
                    + FriendlyType(property.PropertyType) + " " + fqn + indexer + " { "
                    + (property.GetMethod != null && IsPublic(property.GetMethod) ? "get; " : string.Empty)
                    + (property.SetMethod != null && IsPublic(property.SetMethod) ? "set; " : string.Empty)
                    + "}";
                if (!Matches(query, fqn, signature))
                    continue;
                Emit("property", assembly.Name.Name, fqn, signature, type.Namespace, property, type);
                count++;
            }

            foreach (var field in type.Fields)
            {
                if (!IsPublic(field))
                    continue;
                var fqn = typeName + "." + field.Name;
                var signature = Visibility(field) + (field.IsStatic ? " static " : " ")
                    + FriendlyType(field.FieldType) + " " + fqn;
                if (!Matches(query, fqn, signature))
                    continue;
                Emit("field", assembly.Name.Name, fqn, signature, type.Namespace, field, type);
                count++;
            }

            foreach (var eventDefinition in type.Events)
            {
                var accessor = eventDefinition.AddMethod ?? eventDefinition.RemoveMethod;
                if (accessor == null || !IsPublic(accessor))
                    continue;
                var fqn = typeName + "." + eventDefinition.Name;
                var signature = Visibility(accessor) + (accessor.IsStatic ? " static " : " ")
                    + "event " + FriendlyType(eventDefinition.EventType) + " " + fqn;
                if (!Matches(query, fqn, signature))
                    continue;
                Emit("event", assembly.Name.Name, fqn, signature, type.Namespace, eventDefinition, type);
                count++;
            }
        }

        return count > 0 ? 0 : 3;
    }

    private static void AddSearchTree(DefaultAssemblyResolver resolver, string root)
    {
        if (string.IsNullOrEmpty(root) || !Directory.Exists(root))
            return;
        AddSearchDirectory(resolver, root);
        foreach (var directory in Directory.GetDirectories(root, "*", SearchOption.AllDirectories))
            AddSearchDirectory(resolver, directory);
    }

    private static void AddSearchDirectory(DefaultAssemblyResolver resolver, string directory)
    {
        if (!string.IsNullOrEmpty(directory) && Directory.Exists(directory))
            resolver.AddSearchDirectory(directory);
    }

    private static IEnumerable<TypeDefinition> AllTypes(IEnumerable<TypeDefinition> roots)
    {
        foreach (var type in roots)
        {
            yield return type;
            foreach (var nested in AllTypes(type.NestedTypes))
                yield return nested;
        }
    }

    private static bool Matches(string query, params string[] values)
    {
        return values.Any(value =>
        {
            var candidate = NormalizeName(value);
            return candidate == query || candidate.EndsWith("." + query);
        });
    }

    private static string NormalizeName(string value)
    {
        if (string.IsNullOrWhiteSpace(value))
            return string.Empty;
        var result = value.Trim();
        var parameters = result.IndexOf('(');
        if (parameters >= 0)
            result = result.Substring(0, parameters);
        var generic = result.IndexOf('<');
        if (generic >= 0)
            result = result.Substring(0, generic);
        return result.ToLowerInvariant();
    }

    private static bool IsPublic(TypeDefinition type)
    {
        return type.IsPublic || type.IsNestedPublic || type.IsNestedFamily
            || type.IsNestedFamilyOrAssembly;
    }

    private static bool IsPublic(MethodDefinition method)
    {
        return method.IsPublic || method.IsFamily || method.IsFamilyOrAssembly;
    }

    private static bool IsPublic(FieldDefinition field)
    {
        return field.IsPublic || field.IsFamily || field.IsFamilyOrAssembly;
    }

    private static string Visibility(TypeDefinition type)
    {
        return type.IsPublic || type.IsNestedPublic ? "public" : "protected";
    }

    private static string Visibility(MethodDefinition method)
    {
        return method.IsPublic ? "public" : "protected";
    }

    private static string Visibility(FieldDefinition field)
    {
        return field.IsPublic ? "public" : "protected";
    }

    private static string TypeKind(TypeDefinition type)
    {
        if (type.IsInterface) return "interface";
        if (type.IsEnum) return "enum";
        if (type.IsValueType) return "struct";
        if (type.BaseType != null && type.BaseType.FullName == "System.MulticastDelegate") return "delegate";
        return "class";
    }

    private static string GenericParameters(IEnumerable<GenericParameter> parameters)
    {
        var values = parameters.Select(parameter => parameter.Name).ToArray();
        return values.Length == 0 ? string.Empty : "<" + string.Join(", ", values) + ">";
    }

    private static string FormatParameter(ParameterDefinition parameter)
    {
        var prefix = parameter.ParameterType.IsByReference
            ? (parameter.IsOut ? "out " : "ref ")
            : string.Empty;
        var type = parameter.ParameterType.IsByReference
            ? ((ByReferenceType)parameter.ParameterType).ElementType
            : parameter.ParameterType;
        var optional = parameter.HasDefault
            ? " = " + (parameter.Constant == null ? "null" : parameter.Constant.ToString())
            : string.Empty;
        return prefix + FriendlyType(type) + " " + parameter.Name + optional;
    }

    private static string FriendlyDeclaringType(TypeReference type)
    {
        return FriendlyType(type).Replace("/", ".");
    }

    private static string FriendlyType(TypeReference type)
    {
        if (type == null) return "void";
        if (type.IsArray)
        {
            var array = (ArrayType)type;
            return FriendlyType(array.ElementType) + "[" + new string(',', array.Rank - 1) + "]";
        }
        if (type.IsByReference)
            return FriendlyType(((ByReferenceType)type).ElementType);
        if (type.IsPointer)
            return FriendlyType(((PointerType)type).ElementType) + "*";
        if (type is GenericInstanceType)
        {
            var generic = (GenericInstanceType)type;
            return RemoveArity(FriendlyType(generic.ElementType)) + "<"
                + string.Join(", ", generic.GenericArguments.Select(FriendlyType)) + ">";
        }
        if (type is GenericParameter)
            return type.Name;
        return RemoveArity(type.FullName.Replace("/", "."));
    }

    private static string RemoveArity(string value)
    {
        var tick = value.IndexOf('`');
        return tick >= 0 ? value.Substring(0, tick) : value;
    }

    private static void Emit(
        string kind,
        string assembly,
        string fqn,
        string signature,
        string namespaceName,
        ICustomAttributeProvider member,
        ICustomAttributeProvider declaringType)
    {
        var obsolete = FindObsolete(member) ?? FindObsolete(declaringType);
        var message = string.Empty;
        var isError = false;
        if (obsolete != null)
        {
            if (obsolete.ConstructorArguments.Count > 0 && obsolete.ConstructorArguments[0].Value != null)
                message = obsolete.ConstructorArguments[0].Value.ToString();
            if (obsolete.ConstructorArguments.Count > 1 && obsolete.ConstructorArguments[1].Value is bool)
                isError = (bool)obsolete.ConstructorArguments[1].Value;
        }

        Console.WriteLine(string.Join("\t", new[]
        {
            Encode(kind),
            Encode(assembly),
            Encode(fqn),
            Encode(signature),
            Encode(namespaceName ?? string.Empty),
            Encode(obsolete != null ? "true" : "false"),
            Encode(isError ? "true" : "false"),
            Encode(message)
        }));
    }

    private static CustomAttribute FindObsolete(ICustomAttributeProvider provider)
    {
        if (provider == null || !provider.HasCustomAttributes)
            return null;
        return provider.CustomAttributes.FirstOrDefault(
            attribute => attribute.AttributeType.FullName == "System.ObsoleteAttribute");
    }

    private static string Encode(string value)
    {
        return Convert.ToBase64String(Encoding.UTF8.GetBytes(value ?? string.Empty));
    }
}
