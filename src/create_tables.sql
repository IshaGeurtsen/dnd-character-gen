CREATE TABLE IF NOT EXISTS user(id, name, UNIQUE(id));
CREATE TABLE IF NOT EXISTS character(id, user, UNIQUE(id));
CREATE TABLE IF NOT EXISTS PrimaryInfo(
    id,
    PlayerName,
    CharacterName,
    Race,
    ClassLevel,
    Background,
    XP,
    Allignment,
    UNIQUE(id)
);
CREATE TABLE IF NOT EXISTS BaseSkills(id, str, dex, con, int, wis, cha, UNIQUE(id));
CREATE TABLE IF NOT EXISTS QuickRef(
    id,
    inspiration,
    profbonus,
    ac,
    initiative,
    speed,
    hpmax,
    hpcurrent,
    hptemp,
    hd,
    hdtotal,
    passive,
    UNIQUE(id)
);
CREATE TABLE IF NOT EXISTS Skills(
    id,
    Acrobatics,
    Animal,
    Athletics,
    Deception,
    History,
    Insight,
    Intimidation,
    Arcana,
    Investigation,
    Perception,
    Nature,
    Performance,
    Medicine,
    Religion,
    Stealth,
    Persuasion,
    SleightofHand,
    Survival,
    UNIQUE(id)
);
CREATE TABLE IF NOT EXISTS Weapons(id, slot, Name, AtkBonus, Damage, UNIQUE(id));
CREATE TABLE IF NOT EXISTS Purse(id, CP, SP, EP, GP, PP, UNIQUE(id));
CREATE TABLE IF NOT EXISTS FreeFields(
    id,
    PersonalityTraits,
    Ideals,
    Bonds,
    Flaws,
    ProficienciesLang,
    FeaturesAndTraits,
    AttacksSpellcasting,
    Equipment,
    UNIQUE(id)
)