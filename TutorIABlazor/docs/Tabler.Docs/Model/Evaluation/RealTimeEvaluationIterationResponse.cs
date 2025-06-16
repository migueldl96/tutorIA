namespace Tabler.Docs.Model.Evaluation
{
    public class RealTimeEvaluationIterationResponse
    {
        public string state { get; set; }
        public float correct_prob { get; set; }
        public float state_prob { get; set; }
    }
}
