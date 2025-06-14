using System.Collections.Generic;
using Tabler.Docs.Model.Auth;

namespace Tabler.Docs.Model.Dataset
{
    public class StudentSubject
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty; // subject_name
        public int UserId { get; set; }
        public User User { get; set; } = default!;
        public ICollection<StudentSkill> Skills { get; set; } = new List<StudentSkill>();
    }
}
