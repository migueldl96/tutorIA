namespace TutorIA
{
    public partial class RowCol : TablerBaseComponent
    {
        [Parameter] public int Columns { get; set; } = 0;
        [Parameter] public int Xs { get; set; } = 0;
        [Parameter] public int Sm { get; set; } = 0;
        [Parameter] public int Md { get; set; } = 0;
        [Parameter] public int Lg { get; set; } = 0;
        [Parameter] public int Xl { get; set; } = 0;
        [Parameter] public int XXl { get; set; } = 0;
        [Parameter] public bool Auto { get; set; }

        protected override string ClassNames => ClassBuilder
            //.Add("col")
            .Add(BackgroundColor.GetColorClass("bg"))
            .Add(TextColor.GetColorClass("text"))
            .AddIf($"col-{Columns}", Columns > 0)
            .AddIf($"col-xs-{Xs}", Xs > 0)
            .AddIf($"col-sm-{Sm}", Sm > 0)
            .AddIf($"col-md-{Md}", Md > 0)
            .AddIf($"col-lg-{Lg}", Lg > 0)
            .AddIf($"col-xl-{Xl}", Xl > 0)
            .AddIf($"col-xxl-{XXl}", XXl > 0)
            .AddIf("col-auto", Auto)
            .ToString();
    }
}
