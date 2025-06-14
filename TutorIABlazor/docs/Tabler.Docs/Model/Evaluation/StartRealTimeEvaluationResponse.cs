using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace Tabler.Docs.Model.Evaluation
{
    public class StartRealTimeEvaluationResponse
    {
        public string Status { get; set; } = string.Empty;
        public string Message { get; set; } = string.Empty;
        [JsonPropertyName("roster_paths")]
        public Dictionary<string, string> RosterPaths { get; set; } = new();

        public override string ToString()
        {
            return $"Status: {Status}, Message: {Message}, RosterPaths: {string.Join(", ", RosterPaths)}";
        }
    }
}
