namespace Tabler.Docs.Data.QuestionnaireService
{
    public class GenerateQuizResponse
    {
        public Class1[] Property1 { get; set; }
    }

    public class Class1
    {
        public string question { get; set; }
        public string optionA { get; set; }
        public string optionB { get; set; }
        public string optionC { get; set; }
        public string optionD { get; set; }
        public string correct_answer { get; set; }
        public string explanation { get; set; }
        public int page_number { get; set; }
        public string filename { get; set; }
        public string description { get; set; }
        public string uri { get; set; }
    }

}
