using System.Collections.Generic;
using Tabler.Docs.Model.Dataset;

namespace Tabler.Docs.Model.Auth
{
    public class User
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public List<StudentSubject> Subjects { get; set; }
        public int LastQuestionOrderId { get; set; }
    }
}
