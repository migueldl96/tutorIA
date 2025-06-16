namespace Tabler.Docs.Model.Dataset
{
    public class UpdateDatasetRequestBody
    {
        public int order_id { get; set; }
        public string user_id { get; set; }
        public string skill_name { get; set; }
        public int correct { get; set; }
        public string item_id { get; set; }
        public string subject_id { get; set; }
    }
}
