namespace TutorIA
{
    public class ToastOptions
    {
        /// <summary>
        /// Delay in Seconds
        /// Set 0 to show it until manually removed
        /// </summary>
        public int Delay { get; set; } = 3;
        public bool ShowHeader { get; set; } = true;
        public bool ShowProgress { get; set; } = true;
        public bool AllowUserRemove { get; set; } = true;
        public bool AutoClose => Delay > 0;
        public ToastPosition Position { get; set; } = ToastPosition.TopEnd;
    }

    public enum ToastPosition
    {
        TopEnd,
        TopStart,
        BottomEnd,
        BottomStart
    }

}

