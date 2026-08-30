# Initial failures

- Config-authoring helper initially had a syntax typo `else92`; fixed before task execution.
- First standard checker reported missing condition mappings because labels lacked required Markdown backticks; mappings existed and were formatted correctly on repair. No gate weakening.
- Initial source retrieval failures documented in references/source_audit.md.
- An independent TAPS precheck used an incorrect contracts-root path; corrected to E:/Taskbeacon/taps/contracts without contract changes.
- Shared runtime pre-push fetch briefly failed DNS resolution; subsequent non-force push succeeded and fresh fetch plus ls-remote verified origin/main4d866ff003f6d3dc5bca3409b2c73b53f622d884.
- Standalone schedule probe initially ran from workspace root, where the checkout directory shadowed the installed psyflow package; rerunning from the task root succeeded using actual BlockUnit. No runtime source repair needed.
