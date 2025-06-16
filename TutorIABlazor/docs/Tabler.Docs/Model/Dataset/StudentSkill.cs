namespace Tabler.Docs.Model.Dataset
{
    public class StudentSkill
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public float Learn { get; set; }

        public int StudentSubjectId { get; set; }
        public StudentSubject StudentSubject { get; set; } = default!;
    }
}
