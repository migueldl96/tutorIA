using System.Collections.Generic;

namespace Tabler.Docs.Model.Dataset
{
    public class SubjectSkillDetail
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty; // Esta es la propiedad que faltaba
        public int SubjectSkillId { get; set; }
        public SubjectSkill SubjectSkill { get; set; } = default!;
        public List<SkillState> States { get; set; } = new();
    }

}
