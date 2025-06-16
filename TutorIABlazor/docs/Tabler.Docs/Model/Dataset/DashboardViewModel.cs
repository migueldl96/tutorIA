namespace Tabler.Docs.Model.Dataset
{
    public class DashboardViewModel
    {
        public string TeachingUnitName { get; set; }
        public StatusType Status { get; set; }
        public int ProgressBarPercentage { get; set; }
        public int ProgressIconPercentage { get; set; }
    }

    public enum StatusType
    {
        Inactivo,
        En_Progreso,
        Maestria_Alcanzada
    }
}
