import Lake
open Lake DSL

package «seven-magicks» where
  -- Package configuration

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib «SevenMagicks» where
  -- Library configuration
  roots := #[`Canon]
