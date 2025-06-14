using System.Collections.Generic;

namespace Tabler.Docs.Model.Dataset
{

    public class SubjectSkill
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty; // skill_name
        public ICollection<SubjectSkillDetail> SubjectDetails { get; set; } = new List<SubjectSkillDetail>();
    }
}
