use std::hash::{DefaultHasher, Hash, Hasher};

mod ivec2;

pub use self::ivec2::IVec2;

pub fn calculate_hash<T: Hash>(t: &T) -> u64 {
    let mut s = DefaultHasher::new();
    t.hash(&mut s);
    s.finish()
}
