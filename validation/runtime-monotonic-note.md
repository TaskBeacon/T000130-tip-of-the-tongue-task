# Cross-phase timing infrastructure

Task130 exposed onset_time_monotonic_s in shared psyflow-web, commit4d866ff003f6d3dc5bca3409b2c73b53f622d884. Parent reviewed and independently verified before authorized publication. Four runtime files receive11 additive lines; one47-line test contains actual stage Date.now-jump and runtime raw/reduced propagation checks. Existing epoch fields and timing behavior are unchanged. Optional typing preserves compatibility with older synthetic fixtures; real current runtime emits the field on executed stages.

Native resolution uses PsychoPy flip_time+rt; web uses shared performance.now stage onset+rt. Neither is a hardware display-onset calibration. Native flip is a display callback; web onset is the existing keyboard RT origin after DOM construction. Cross-platform perceptual onset precision is not claimed identical. H130 must fail explicitly if monotonic onset required for resolution is unavailable; it must not silently fall back to wall-clock epochs.

Validation:18coretestsPASS,scope includes public runtime and new test TypeScriptPASS,productionbuildPASS. Both raw stage output and reduced prefixed field preserve the monotonic field. Runtime remote/main verified after nonforcepush. Two generated manifest files were intentionally excluded from commit.
