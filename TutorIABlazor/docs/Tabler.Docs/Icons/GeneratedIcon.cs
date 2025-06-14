using System.Collections.Generic;
using System.Linq;
using TutorIA;

namespace Tabler.Docs.Icons
{
    public class GeneratedIcon
    {
        public string Name { get; set; }
        public string Author { get; set; }
        public List<string> Tags { get; set; }
        public IIconType IconType { get; set; }
        public string DotNetProperty => $"public static IIconType {GetSafeName()} => new {IconType.ClassName}(@\"{IconType?.Elements}\", {IconType.Filled.ToString().ToLower()});";

        public string DotNetProperty2
        {
            get
            {
                if (IconType.Filled)
                {
                    return $"public static IIconType {GetSafeName()} => new {IconType.ClassName}(@\"{IconType?.Elements}\", {IconType.Filled.ToString().ToLower()});";

                }
                return $"public static IIconType {GetSafeName()} => new {IconType.ClassName}(@\"{IconType?.Elements}\");";
            }
        }

        public string GetSafeName()
        {
            var safeName = Name;
            safeName = safeName.Replace("-", "_");
            if (char.IsDigit(safeName.ToCharArray().First()))
            {
                safeName = "_" + safeName;
            }
            else
            {
                safeName = FirstCharacterToUpperCase(safeName);
            }

            return safeName;
        }


        private static string FirstCharacterToUpperCase(string text)
        {
            if (string.IsNullOrWhiteSpace(text)) { return text; }

            if (text.Length == 1)
            {
                return char.ToUpper(text[0]).ToString();
            }

            return char.ToUpper(text[0]) + text.Substring(1);
        }

    }



}

