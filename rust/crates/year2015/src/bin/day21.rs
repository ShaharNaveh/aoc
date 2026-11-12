use std::ops::{Add, Deref, DerefMut, Not};

use util::{Day, aoc_main};

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct Stats {
    damage: usize,
    armor: usize,
}

impl Stats {
    const EMPTY: Self = Self {
        damage: 0,
        armor: 0,
    };
}

impl Add<Self> for Stats {
    type Output = Self;

    fn add(self, rhs: Self) -> Self::Output {
        Self {
            damage: self.damage + rhs.damage,
            armor: self.armor + rhs.armor,
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct Item {
    cost: usize,
    stats: Stats,
}

impl Item {
    const EMPTY: Self = Self {
        cost: 0,
        stats: Stats::EMPTY,
    };
}

impl Add<Self> for Item {
    type Output = Self;

    fn add(self, rhs: Self) -> Self::Output {
        Self {
            cost: self.cost + rhs.cost,
            stats: self.stats + rhs.stats,
        }
    }
}

impl From<&str> for Item {
    fn from(value: &str) -> Self {
        let nums = value
            .trim()
            .split_ascii_whitespace()
            .filter(|s| !s.contains('+'))
            .filter_map(|s| s.parse().ok())
            .collect::<Vec<_>>();

        Self {
            cost: nums[0],
            stats: Stats {
                damage: nums[1],
                armor: nums[2],
            },
        }
    }
}

#[derive(Clone, Copy, Debug)]
struct Items<const N: usize>([Item; N]);

impl<const N: usize> Deref for Items<N> {
    type Target = [Item; N];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<const N: usize> From<&str> for Items<N> {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .lines()
                .filter_map(|line| (!line.contains(':')).then(|| line.into()))
                .collect::<Vec<_>>()
                .try_into()
                .unwrap(),
        )
    }
}

#[derive(Clone, Copy, Debug)]
struct ItemShop {
    weapons: Items<5>,
    armor: Items<5>,
    rings: Items<6>,
}

impl ItemShop {
    fn items(&self) -> impl Iterator<Item = Item> + '_ {
        self.weapons.iter().flat_map(move |&weapon| {
            std::iter::once(Item::EMPTY)
                .chain(self.armor.iter().copied()) // 6 armor choices
                .flat_map(move |armor| {
                    let n = self.rings.len();
                    std::iter::once(Item::EMPTY)
                        .chain(self.rings.iter().copied())
                        .chain((0..n).flat_map(move |i| {
                            (i + 1..n).map(move |j| self.rings[i] + self.rings[j])
                        }))
                        .map(move |ring| weapon + armor + ring)
                })
        })
    }
}

impl From<&str> for ItemShop {
    fn from(value: &str) -> Self {
        let chunks = value.trim().split("\n\n").collect::<Vec<_>>();
        Self {
            weapons: chunks[0].into(),
            armor: chunks[1].into(),
            rings: chunks[2].into(),
        }
    }
}

impl Default for ItemShop {
    fn default() -> Self {
        "
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"
        .into()
    }
}

#[derive(Clone, Copy, Debug)]
struct Entity {
    hp: usize,
    stats: Stats,
}

#[derive(Clone, Copy, Debug)]
struct Boss(Entity);

impl Deref for Boss {
    type Target = Entity;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Boss {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl From<Entity> for Boss {
    fn from(value: Entity) -> Self {
        Self(value)
    }
}

impl From<&str> for Boss {
    fn from(value: &str) -> Self {
        let nums = value
            .trim()
            .split_ascii_whitespace()
            .filter_map(|s| s.parse().ok())
            .collect::<Vec<_>>();

        Entity {
            hp: nums[0],
            stats: Stats {
                damage: nums[1],
                armor: nums[2],
            },
        }
        .into()
    }
}

#[derive(Clone, Copy, Debug)]
struct Player(Entity);

impl Player {
    fn new(stats: Stats) -> Self {
        Entity { hp: 100, stats }.into()
    }
}

impl From<Entity> for Player {
    fn from(value: Entity) -> Self {
        Self(value)
    }
}

impl Deref for Player {
    type Target = Entity;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Player {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

#[derive(Clone, Copy, Debug)]
struct Game {
    player: Player,
    boss: Boss,
}

impl Game {
    const fn new(player: Player, boss: Boss) -> Self {
        Self { player, boss }
    }

    /// Returns the winner.
    fn simulate(self) -> EntityType {
        let mut turn = EntityType::Player;

        let Self {
            mut player,
            mut boss,
        } = self;

        let boss_damage = boss
            .stats
            .damage
            .checked_sub(player.stats.armor)
            .unwrap_or(1);

        let player_damage = player
            .stats
            .damage
            .checked_sub(boss.stats.armor)
            .unwrap_or(1);

        loop {
            match turn {
                EntityType::Boss => {
                    player.hp = if let Some(nhp) = player.hp.checked_sub(boss_damage) {
                        nhp
                    } else {
                        return turn;
                    }
                }
                EntityType::Player => {
                    boss.hp = if let Some(nhp) = boss.hp.checked_sub(player_damage) {
                        nhp
                    } else {
                        return turn;
                    }
                }
            }

            turn = !turn;
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum EntityType {
    Boss,
    Player,
}

impl Not for EntityType {
    type Output = Self;

    fn not(self) -> Self::Output {
        match self {
            Self::Player => Self::Boss,
            Self::Boss => Self::Player,
        }
    }
}

struct Analysis {
    min_win_gold: usize,
    max_lose_gold: usize,
}

impl Analysis {
    fn new(boss: Boss, item_shop: ItemShop) -> Self {
        let mut min_win_gold = None;
        let mut max_lose_gold = None;

        for item in item_shop.items() {
            let Item { cost, stats } = item;

            let game = Game::new(Player::new(stats), boss);

            if min_win_gold.is_none_or(|v| cost < v) && game.simulate() == EntityType::Player {
                min_win_gold = Some(cost);
            }

            if max_lose_gold.is_none_or(|v| cost > v) && game.simulate() == EntityType::Boss {
                max_lose_gold = Some(cost);
            }
        }

        Self {
            min_win_gold: min_win_gold.unwrap(),
            max_lose_gold: max_lose_gold.unwrap(),
        }
    }
}

struct Day21;

impl Day for Day21 {
    type Parsed = Boss;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        Analysis::new(*input, ItemShop::default()).min_win_gold
    }

    fn part2(input: &Self::Parsed) -> usize {
        Analysis::new(*input, ItemShop::default()).max_lose_gold
    }
}

aoc_main!(Day21);

#[cfg(test)]
mod tests {
    use super::*;

    /// Number of ways to choose k items from n.
    fn choose(n: usize, k: usize) -> usize {
        if k > n {
            return 0;
        }
        (0..k).fold(1, |acc, i| acc * (n - i) / (i + 1))
    }

    #[test]
    fn items() {
        let shop = ItemShop::default();

        let (weapons, armor, rings) = (shop.weapons.len(), shop.armor.len(), shop.rings.len());

        assert_eq!(
            shop.items().count(),
            choose(weapons, 1)
                * (0..=1).into_iter().map(|k| choose(armor, k)).sum::<usize>()
                * (0..=2).into_iter().map(|k| choose(rings, k)).sum::<usize>()
        );
    }

    #[test]
    fn part1() {
        let game = Game {
            player: Entity {
                hp: 8,
                stats: Stats {
                    damage: 5,
                    armor: 5,
                },
            }
            .into(),
            boss: Entity {
                hp: 12,
                stats: Stats {
                    damage: 7,
                    armor: 2,
                },
            }
            .into(),
        };

        assert_eq!(game.simulate(), EntityType::Player);
    }
}
