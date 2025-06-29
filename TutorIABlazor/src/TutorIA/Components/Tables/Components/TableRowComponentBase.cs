namespace TutorIA.Components.Tables
{
    public abstract class TableRowComponentBase<TableItem> : ComponentBase
    {
        public string GetColumnWidth(IColumn<TableItem> column)
        {
            return !string.IsNullOrEmpty(column.Width) ? $"width:{column.Width}; " : null;
        }

        public virtual string GetColumnClass(IColumn<TableItem> column)
        {
            return new ClassBuilder()
                .Add(column.CssClass)
                .AddIf("text-end", column.Align == Align.End)
                .ToString();
        }
    }
}
