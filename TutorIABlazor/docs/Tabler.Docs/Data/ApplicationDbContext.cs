using Microsoft.EntityFrameworkCore;
using Tabler.Docs.Data;
using Tabler.Docs.Model.Auth;
using Tabler.Docs.Model.Dataset;
using Tabler.Docs.Model.Questionnaire;

public class ApplicationDbContext : DbContext
{
    public DbSet<Country> Countries { get; set; } = default!;
    public DbSet<User> Users { get; set; } = default!;
    public DbSet<QuestionBase> QuestionBases { get; set; } = default!;
    public DbSet<AnswerOption> AnswerOptions { get; set; } = default!;
    public DbSet<StudentSubject> StudentSubjects { get; set; } = default!;
    public DbSet<StudentSkill> StudentSkills { get; set; } = default!;
    public DbSet<SubjectSkill> SubjectSkills { get; set; } = default!;
    public DbSet<SubjectSkillDetail> Subjects { get; set; } = default!;
    public DbSet<SkillState> SubjectStates { get; set; } = default!;

    public ApplicationDbContext(DbContextOptions options) : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Country>().HasKey(x => x.Code);
        modelBuilder.Entity<Country>().OwnsOne(x => x.Medals);
        modelBuilder.Entity<QuestionBase>()
    .HasDiscriminator<string>("Discriminator")
    .HasValue<UniqueChoiceQuestion>("UniqueChoiceQuestion");

        modelBuilder.Entity<UniqueChoiceQuestion>()
            .HasMany(q => q.Options)
            .WithOne(o => o.Question)
            .HasForeignKey(o => o.QuestionId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity<User>()
        .HasMany(u => u.Subjects)
        .WithOne(s => s.User)
        .HasForeignKey(s => s.UserId)
        .OnDelete(DeleteBehavior.Cascade);

        // StudentSubject
        modelBuilder.Entity<StudentSubject>()
            .HasKey(s => s.Id);

        modelBuilder.Entity<StudentSubject>()
            .HasMany(s => s.Skills)
            .WithOne(sk => sk.StudentSubject)
            .HasForeignKey(sk => sk.StudentSubjectId)
            .OnDelete(DeleteBehavior.Cascade);

        // StudentSkill
        modelBuilder.Entity<StudentSkill>()
            .HasKey(sk => sk.Id);

        // SubjectSkill (global skill)
        modelBuilder.Entity<SubjectSkill>()
            .HasKey(ss => ss.Id);

        modelBuilder.Entity<SubjectSkill>()
            .HasMany(ss => ss.SubjectDetails)
            .WithOne(d => d.SubjectSkill)
            .HasForeignKey(d => d.SubjectSkillId)
            .OnDelete(DeleteBehavior.Cascade);

        // SubjectSkillDetail (subject_skill_name)
        modelBuilder.Entity<SubjectSkillDetail>()
            .HasKey(d => d.Id);

        modelBuilder.Entity<SubjectSkillDetail>()
            .HasMany(d => d.States)
            .WithOne(s => s.SubjectSkillDetail)
            .HasForeignKey(s => s.SubjectSkillDetailId)
            .OnDelete(DeleteBehavior.Cascade);

        // SkillState
        modelBuilder.Entity<SkillState>()
            .HasKey(s => s.Id);
    }
}
