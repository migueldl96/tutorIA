namespace TutorIA
{
    public class ResizeObserverEntry
    {
        public ContentRect ContentRect { get; set; }
    }

    public class ContentRect
    {
        public double X { get; set; }
        public double Y { get; set; }
        public double Width { get; set; }
        public double Height { get; set; }
        public double Top { get; set; }
        public double Right { get; set; }
        public double Bottom { get; set; }
        public double Left { get; set; }
    }
}

