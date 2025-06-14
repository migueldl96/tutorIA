using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace Tabler.Docs.Model.Dataset
{
    public class UpdateDatasetResponseBody
    {
        [JsonExtensionData]
        public List<Class1> Items { get; set; } = new();
    }

    public class Class1
    {
        public Students_States[] students_states { get; set; }
        public Skills_States[] skills_states { get; set; }
    }

    public class Students_States
    {
        public string id { get; set; }
        public Student_Subject_List[] student_subject_list { get; set; }
    }

    public class Student_Subject_List
    {
        public string subject_name { get; set; }
        public Student_Skill_List[] student_skill_list { get; set; }
    }

    public class Student_Skill_List
    {
        public string name { get; set; }
        public float learn { get; set; }
    }

    public class Skills_States
    {
        public string skill_name { get; set; }
        public Subject_Skill_List[] subject_skill_list { get; set; }
    }

    public class Subject_Skill_List
    {
        public string subject_skill_name { get; set; }
        public State[] states { get; set; }
    }

    public class State
    {
        public string name { get; set; }
        public float value { get; set; }
    }

}
