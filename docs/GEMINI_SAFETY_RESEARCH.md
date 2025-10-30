# Gemini API Safety Filter Issue - Detailed Research Brief

## Problem Summary
Google Gemini API models (including 1.5-flash, 2.0-flash, and 2.5-flash/pro) are blocking harmless Arabic customer service conversations with `finish_reason: 2` (SAFETY), even when all safety settings are configured to `BLOCK_NONE`.

## Technical Details

### Error Pattern
```python
finish_reason: 2  # SAFETY block
# Error: The response.text quick accessor requires the response to contain a valid Part, 
# but none were returned. The candidate's [finish_reason] is 2.
```

### Configuration Attempted
```python
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]
```

**Result**: Settings ignored or overridden - content still blocked

### Test Case That Failed
**Context**: LLM-to-LLM interaction simulating Egyptian customer service
- **Domain**: E-commerce delivery inquiry
- **Language**: Egyptian Arabic dialect
- **Content**: Completely benign customer-agent dialogue
- **Issue**: Blocked at various conversation turns (turn 1 or turn 2)

**Example Blocked Content**:
```
Customer: "السلام عليكم، معرفة حالة الطلب ومتى سيصل الموبايل بالضبط، محتاجه لاجتماع مهم"
(Translation: "Peace be upon you, I need to know the order status and when the mobile will arrive exactly, I need it for an important meeting")
```

**Why this is problematic**: This is standard, polite, professional customer service language with zero harmful content.

## Root Causes (Research Needed)

### 1. **Non-Configurable Safety Filters**
According to [Google Cloud Community discussions](https://discuss.ai.google.dev/t/safety-settings-error/79337), Gemini has:
- **Configurable filters**: Can be set to BLOCK_NONE (harassment, hate speech, sexual, dangerous)
- **Non-configurable filters**: ALWAYS active (CSAM, PII, etc.) - CANNOT be disabled

**Hypothesis**: Arabic text may be incorrectly triggering non-configurable filters due to:
- Poor training data representation for Arabic
- Pattern matching errors in Arabic script
- Cultural/linguistic context misunderstanding

### 2. **Arabic-Specific Issues**
- **Script complexity**: Arabic uses connected letters, diacritics, and bidirectional text
- **Dialect variation**: Egyptian Arabic differs significantly from Modern Standard Arabic (MSA)
- **Training data bias**: Gemini's training may have limited Egyptian dialect data
- **False positive patterns**: Common Arabic phrases may match harmful content patterns from other contexts

### 3. **Multi-Turn Conversation Context**
- Safety filters evaluate cumulative conversation context
- Long conversations with multiple turns accumulate "risk scores"
- Arabic conversations may score higher due to misclassification

### 4. **Model Version Differences**
Tested models and their behavior:
- **gemini-2.5-pro**: Blocked frequently, both customer and agent
- **gemini-2.5-flash**: Blocked frequently, inconsistent
- **gemini-1.5-flash**: More stable but still occasional blocks
- **gemini-2.0-flash-exp**: Blocked on turn 1 or 2

**Pattern**: Newer models (2.5 series) are MORE restrictive, not less

## Evidence from Testing

### Successful Test (Claude 3.5 Haiku)
**Same exact scenario, same exact prompts:**
- ✅ 6 full conversation turns
- ✅ Natural Egyptian Arabic
- ✅ Zero safety blocks
- ✅ 26,582 tokens, 46 seconds
- ✅ Proper empathy, problem-solving, cultural fit

**Conclusion**: The content itself is NOT harmful - only Gemini is blocking it.

### Failed Tests (Gemini)
- **Attempt 1** (gemini-2.5-pro): Blocked on customer turn 1
- **Attempt 2** (gemini-2.5-flash): Blocked on agent turn 2
- **Attempt 3** (gemini-1.5-flash): Needs testing
- **Common pattern**: Blocks occur EARLY (turns 1-2) in INNOCENT conversations

## Questions for AI Research Agent

### Technical Investigation
1. **What are the specific non-configurable safety filters in Gemini API?**
   - What categories cannot be disabled?
   - How do they evaluate Arabic text?
   - Is there PII detection that misclassifies Arabic names/addresses?

2. **What is Gemini's Arabic language training data composition?**
   - What percentage is Egyptian Arabic vs MSA?
   - What domains are represented (news, social media, formal text)?
   - Is customer service dialogue underrepresented?

3. **Are there documented issues with Gemini and Arabic safety filters?**
   - GitHub issues, bug reports, or community discussions
   - Google AI forum posts about Arabic false positives
   - Any official Google responses or workarounds

4. **How do safety filters score multi-turn conversations?**
   - Is it cumulative or per-message?
   - Can early messages "poison" later turns?
   - Is there a conversation-level risk threshold?

### Comparison Research
5. **Why does Claude 3.5 Haiku handle this perfectly?**
   - Different safety filter architecture?
   - Better Arabic training data?
   - More sophisticated cultural context understanding?

6. **How do other major LLM providers (OpenAI, Cohere, Mistral) handle Arabic safety filtering?**
   - Do they have similar issues?
   - What are their configuration options?

### Workarounds and Solutions
7. **Are there API parameters or system instructions that help?**
   - Vertex AI vs AI Studio API differences?
   - Using `system_instruction` vs `safety_settings`
   - Pre-prompting to establish context?

8. **Is there a Gemini model variant better for Arabic?**
   - Gemini 1.5 vs 2.0 vs 2.5 series
   - Flash vs Pro models
   - Experimental vs stable versions

9. **Can we use prompt engineering to avoid false positives?**
   - Framing Arabic content with English context?
   - Explicit "this is customer service training data" disclaimers?
   - Structured format (JSON, XML) to signal non-harmful intent?

10. **Is there an enterprise/paid tier with different safety controls?**
    - Vertex AI vs public API differences
    - Request whitelisting or custom safety policies
    - Contact point for false positive reports

## Impact on Project

### Current Status
- **Claude 3.5 Haiku**: ✅ Working perfectly - PRIMARY MODEL
- **Gemini**: ❌ Unreliable for Arabic customer service evaluation
- **Qwen (W&B Inference)**: ⏳ Testing in progress

### Evaluation Plan
Given the Gemini issues:
1. **Primary**: Claude 3.5 Haiku (proven, reliable)
2. **Secondary**: Qwen 3 235B (open-source alternative)
3. **Tertiary**: Gemini 1.5-flash (if testing shows improvement)

### Research Goal
Determine if Gemini can be made reliable for Arabic customer service evaluation, or if it should be excluded from the benchmark suite entirely.

## References and Resources
- [Google AI Safety Settings Documentation](https://ai.google.dev/gemini-api/docs/safety-settings)
- [Google Cloud: Content Filters and System Instructions](https://cloud.google.com/blog/products/ai-machine-learning/enhance-gemini-model-security-with-content-filters-and-system-instructions)
- [Community Report: Safety Settings Not Working](https://discuss.ai.google.dev/t/safety-settings-error/79337)
- [W&B Qwen3-Coder Inference Tutorial](https://wandb.ai/wandb_fc/genai-research/reports/Tutorial-Run-inference-with-Qwen3-Coder-using-W-B-Inference--VmlldzoxNDM5MDY1Nw)

## Desired Outcome
Find a reliable configuration or alternative approach that allows:
- ✅ Multi-turn Arabic customer service conversations
- ✅ Egyptian dialect support
- ✅ No false positive safety blocks
- ✅ Consistent performance across all 10 scenarios
- ✅ Suitable for publishing evaluation results