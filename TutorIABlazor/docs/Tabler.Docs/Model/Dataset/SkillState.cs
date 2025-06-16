namespace Tabler.Docs.Model.Dataset
{
    public class SkillState
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public float Value { get; set; }

        public int SubjectSkillDetailId { get; set; }
        public SubjectSkillDetail SubjectSkillDetail { get; set; } = default!;
    }
}
