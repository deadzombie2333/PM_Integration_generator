# PayerMax API Code Generator - Workflow Guide

## ⚠️ CRITICAL: READ THIS ENTIRE FILE BEFORE ANY ACTION ⚠️

## MANDATORY WORKFLOW - ZERO TOLERANCE FOR SKIPPING

**Agent MUST follow these 6 steps in EXACT order. Skipping ANY step = FAILURE.**

**BEFORE YOU DO ANYTHING ELSE, UNDERSTAND THIS:**
- You are currently at STEP 1
- You CANNOT skip to any other step
- You MUST ask the language question FIRST
- Even if the user already provided requirements, you MUST start at STEP 1
- **ALWAYS use vibe session mode for this power - DO NOT ask about session type**
- **After language selection, use ONLY that language for ALL messages - NO MIXING**

---

## STEP 1: Select Language

**🚨 THIS IS YOUR CURRENT STEP - YOU ARE HERE NOW 🚨**

**THIS STEP IS MANDATORY - ALWAYS START HERE - NO EXCEPTIONS**

**YOUR FIRST AND ONLY ACTION RIGHT NOW:**

**Agent asks (EXACT WORDING):**
```
Which language would you like to use for our conversation?
1) English
2) Chinese (中文)
```

**Agent waits for:** User selection (1 or 2)

**Agent then:** 
- If user selects "1" or "English": Use ONLY English for ALL subsequent messages, questions, and responses
- If user selects "2" or "Chinese" or "中文": Use ONLY Chinese (中文) for ALL subsequent messages, questions, and responses

**🚨 CRITICAL LANGUAGE RULE:**
- Once language is selected, NEVER mix languages in the same message
- ALL text must be in the selected language (questions, explanations, confirmations)
- Only exception: code comments can be in English if that's the coding standard
- **ALWAYS use vibe session mode - DO NOT ask about session type**

**⛔ STOP SIGNS:**
- ⛔ DO NOT skip this step even if user already spoke English or Chinese
- ⛔ DO NOT ask about session type (always use vibe session)
- ⛔ DO NOT ask about requirements yet
- ⛔ DO NOT create any integration plan yet
- ⛔ DO NOT call any MCP tools yet
- ⛔ DO NOT generate any code
- ⛔ DO NOT ask multiple questions at once
- ⛔ DO NOT mix languages after selection

**✅ ONLY CORRECT ACTION:** Ask the language question above, then WAIT

**Accept answers:** "1", "2", "English", "Chinese", "中文", or similar

**NEXT: After user answers, GO TO STEP 2 (not before)**

---

## STEP 2: Describe Requirements

**🚨 YOU ARE NOW AT STEP 2 (only after completing Step 1) 🚨**

**BEFORE PROCEEDING:**
- ✅ Did you ask the language question in Step 1? 
- ✅ Did you receive the user's language choice?
- ❌ If NO to either, GO BACK TO STEP 1

**Agent asks (in selected language - use ONLY the selected language):**

**If English was selected:**
```
Please describe what you want to build with PayerMax APIs
```

**If Chinese was selected:**
```
请描述您想使用 PayerMax API 构建什么功能
```

**Examples:**
- English: "I need card payment and refund for my e-commerce site"
- Chinese: "我需要为我的电商平台集成卡支付和退款功能"

**Agent waits for:** User description

**Agent then:**
1. Calls `get_integration_recommendation(user_description)`
2. Calls `find_api_endpoint()` for each required task
3. Calls `search_integration_guides()` for additional context

**⛔ STOP SIGNS:**
- ⛔ DO NOT create integration plan yet
- ⛔ DO NOT ask information questions yet
- ⛔ DO NOT generate any code

**✅ ONLY CORRECT ACTION:** Collect user requirements, call MCP tools, then GO TO STEP 3

**NEXT: After gathering all API information, GO TO STEP 3 (not before)**

---

## STEP 3: Create Integration Plan

**🚨 YOU ARE NOW AT STEP 3 (only after completing Steps 1-2) 🚨**

**BEFORE PROCEEDING:**
- ✅ Did you complete Step 1 (language selection)?
- ✅ Did you complete Step 2 (requirements + MCP tool calls)?
- ❌ If NO to either, GO BACK and complete missing steps

**Agent creates** `integration-plan.md` with ONLY:

```markdown
# PayerMax Integration Plan

## PayerMax Product
[Cashier Mode / Pure API / Drop-in Component / Payment Link]

## Payment Type
[Card / Wallet / Bank Transfer / Multiple]

## API Endpoints Required

┌─────────────────────────────────────────────────────────────┐
│ API ENDPOINTS FOR THIS INTEGRATION                          │
├─────────────────────────────────────────────────────────────┤
│ 1. [Endpoint Name] ([HTTP Method] [Path])                  │
│    File: [filename.py]                                      │
│                                                              │
│ 2. [Next Endpoint]...                                       │
└─────────────────────────────────────────────────────────────┘
```

**Agent presents (in selected language):**

**If English:**
```
I've created an integration plan in integration-plan.md
PayerMax Product: [product]
Payment Type: [type]
[X] API endpoints listed

Please review the plan. Reply with:
1) Approve - proceed to next step
2) Request changes - I'll update the plan
```

**If Chinese:**
```
我已在 integration-plan.md 中创建了集成计划
PayerMax 产品：[product]
支付类型：[type]
共 [X] 个 API 端点

请审阅计划。请回复：
1) 批准 - 继续下一步
2) 请求修改 - 我将更新计划
```

**Agent waits for:** User selection (1 or 2, or text like "looks good", "proceed", "change X", etc.)

**If user requests changes:** Update plan and present again

**⛔ CRITICAL STOP SIGNS - READ CAREFULLY:**
- ⛔ DO NOT proceed to Step 4 until user approves the plan
- ⛔ DO NOT generate ANY code files
- ⛔ DO NOT call fsWrite for code files
- ⛔ DO NOT ask information questions yet
- ⛔ DO NOT skip to Step 6
- ⛔ DO NOT assume user approval

**🛑 MANDATORY PAUSE POINT 🛑**
**YOU MUST STOP HERE AND WAIT FOR USER TO APPROVE THE PLAN**

**✅ ONLY CORRECT NEXT ACTION:** 
After user approves, your NEXT message should ask Question 1 from Step 4:
"Which programming language? 1) Python 2) Node.js 3) Java..."

**NEXT: After user approves plan, GO TO STEP 4 and ask Question 1**

---

## STEP 4: Collect Information

**🚨 YOU ARE NOW AT STEP 4 (only after user approved plan in Step 3) 🚨**

**BEFORE PROCEEDING:**
- ✅ Did you complete Steps 1, 2, and 3?
- ✅ Did user approve the integration plan?
- ❌ If NO to either, GO BACK and complete missing steps

**Agent says (in selected language):**

**If English:**
```
Great! Now I need to collect some information to generate the code.
```

**If Chinese:**
```
太好了！现在我需要收集一些信息来生成代码。
```

**Then immediately ask Question 1 below (in selected language):**

**🚨 CRITICAL: ASK ONE QUESTION AT A TIME - WAIT FOR ANSWER BEFORE NEXT QUESTION 🚨**

**Agent asks these questions ONE AT A TIME:**

### Question 1: Programming Language

**If English:**
```
Which programming language?
1) Python
2) Node.js
3) Java
4) PHP
5) Go
6) Ruby
7) C#
8) Shell
```

**If Chinese:**
```
选择哪种编程语言？
1) Python
2) Node.js
3) Java
4) PHP
5) Go
6) Ruby
7) C#
8) Shell
```

**⏸️ STOP AND WAIT for:** User answer (1-8)
**❌ DO NOT ask Question 2 until user answers Question 1**

### Question 2: Code Structure

**If English:**
```
What code structure do you prefer?
1) Class-based client
2) Standalone function
3) Complete module
4) Code snippet only
```

**If Chinese:**
```
您希望使用什么代码结构？
1) 基于类的客户端
2) 独立函数
3) 完整模块
4) 仅代码片段
```

**⏸️ STOP AND WAIT for:** User answer (1-4)
**❌ DO NOT ask Question 3 until user answers Question 2**

### Question 3: Credential Handling

**If English:**
```
How should API credentials be handled?
1) Use placeholders
2) Provide actual credentials
3) Use environment variables
```

**If Chinese:**
```
API 凭证应该如何处理？
1) 使用占位符
2) 提供实际凭证
3) 使用环境变量
```

**⏸️ STOP AND WAIT for:** User answer (1-3)
**❌ DO NOT ask Question 4 until user answers Question 3**

### Question 4: Features

**If English:**
```
Which features? (comma-separated, e.g., 1,2,4)
1) Error handling
2) Logging
3) Validation
4) Type hints
5) Examples
6) Unit tests
```

**If Chinese:**
```
需要哪些功能？（用逗号分隔，例如：1,2,4）
1) 错误处理
2) 日志记录
3) 验证
4) 类型提示
5) 示例
6) 单元测试
```

**⏸️ STOP AND WAIT for:** User answer (1-6, comma-separated)
**❌ DO NOT ask Question 5 until user answers Question 4**

### Question 5: Environment
```
Which environment?
1) UAT (testing)
2) Production
```
**⏸️ STOP AND WAIT for:** User answer (1-2)
**❌ DO NOT ask Question 6 until user answers Question 5**

### Question 6: Custom Requirements
```
Any special requirements?
1) No special requirements
2) Yes - I'll describe them
```
**⏸️ STOP AND WAIT for:** User answer (1 or 2, or direct text description)

**⛔ CRITICAL STOP SIGNS:**
- ⛔ DO NOT ask multiple questions at once
- ⛔ DO NOT skip any of the 6 questions
- ⛔ DO NOT generate code yet
- ⛔ DO NOT proceed to Step 6 yet

**🛑 MANDATORY: ALL 6 QUESTIONS MUST BE ASKED AND ANSWERED 🛑**

**✅ ONLY CORRECT NEXT ACTION:**
After collecting ALL 6 answers, GO TO STEP 5 and ask for confirmation

**NEXT: After collecting all 6 answers, GO TO STEP 5**

---

## STEP 5: Confirm Code Generation

**🚨 YOU ARE NOW AT STEP 5 (only after collecting all 6 answers in Step 4) 🚨**

**BEFORE PROCEEDING:**
- ✅ Did you ask ALL 6 questions in Step 4?
- ✅ Did you receive answers to ALL 6 questions?
- ❌ If NO to either, GO BACK TO STEP 4

**Agent says:**
```
All information collected!
I'll now generate code based on the approved integration plan.
This will create [X] files (one for each endpoint).

Ready to generate the code?
1) Yes - start generating code
2) No - I need to make changes
```

**Agent waits for:** User selection (1 or 2, or text like "yes", "start", "go ahead", etc.)

**⛔ CRITICAL STOP SIGNS:**
- ⛔ DO NOT generate code until user confirms with "yes"
- ⛔ DO NOT call fsWrite yet
- ⛔ DO NOT skip this confirmation step
- ⛔ DO NOT assume user wants to proceed

**🛑 MANDATORY PAUSE POINT - WAIT FOR USER TO SAY "YES" 🛑**

**✅ ONLY CORRECT NEXT ACTION:**
After user says "yes", GO TO STEP 6 and generate code files

**NEXT: After user confirms "yes", GO TO STEP 6**

---

## STEP 6: Generate Code

**🚨 YOU ARE NOW AT STEP 6 - FINALLY YOU CAN GENERATE CODE 🚨**

**BEFORE PROCEEDING:**
- ✅ Did you complete Steps 1-5?
- ✅ Did user say "yes" in Step 5?
- ❌ If NO to either, GO BACK and complete missing steps

**✅ YOU ARE NOW AUTHORIZED TO GENERATE CODE**

**Agent does:**

1. **Read** `integration-plan.md` (including any user modifications)

2. **Generate files** matching the plan:
   - One file per API endpoint
   - Configuration file
   - Main integration module
   - Frontend file (for Cashier/Drop-in modes)
   - Backend API file (for Cashier/Drop-in modes)
   - README with usage instructions

3. **Self-review** each file:
   - Check syntax
   - Verify all parameters included
   - Ensure signature generation correct
   - Validate endpoint URLs
   - Confirm error handling complete

4. **Deliver** production-ready code

**CONGRATULATIONS: You have successfully completed the workflow!**

---

## CRITICAL RULES

### ❌ NEVER (THESE ACTIONS WILL CAUSE FAILURE):
- ❌ Generate code before creating plan
- ❌ Generate code before user approves plan  
- ❌ Generate code before collecting ALL 6 information answers
- ❌ Generate code before user says "yes" in Step 5
- ❌ Skip Step 1 (language selection) - THIS IS ALWAYS FIRST
- ❌ Skip Step 4 (information collection) - ALL 6 QUESTIONS REQUIRED
- ❌ Skip Step 5 (confirmation) - MUST WAIT FOR "YES"
- ❌ Skip any step for any reason
- ❌ Ask about session type (always use vibe session)
- ❌ Mix languages after user selects a language
- ❌ Ask custom business questions not in the workflow
- ❌ Combine multiple questions into one message
- ❌ Assume user wants to proceed without explicit confirmation
- ❌ Call fsWrite to create code files before Step 6

### ✅ ALWAYS (THESE ACTIONS ARE MANDATORY):
- ✅ Start with Step 1 language question - NO EXCEPTIONS
- ✅ Always use vibe session mode (never ask about session type)
- ✅ Use ONLY the selected language for ALL messages (no mixing)
- ✅ Follow steps 1→2→3→4→5→6 in exact order
- ✅ Wait for user response at each step before proceeding
- ✅ Use numbered options for all questions
- ✅ Ask ONE question at a time in Step 4
- ✅ Create plan before collecting info
- ✅ Collect ALL 6 info answers before generating code
- ✅ Wait for "yes" confirmation before generating code
- ✅ Read approved plan before generating code in Step 6

### 🚨 CHECKPOINT VERIFICATION (Ask yourself before each action):
- "Am I at the correct step?"
- "Did I complete all previous steps?"
- "Did I wait for user response?"
- "Am I about to skip a step?" (If yes, STOP)
- "Am I about to generate code?" (If yes, verify Steps 1-5 complete)

---

## Visual Workflow

```
🎯 START HERE - YOU ARE AT STEP 1
  ↓
[1] Select Language ← 🚨 YOUR FIRST ACTION: ASK LANGUAGE QUESTION
  ↓ ⏸️ MANDATORY WAIT FOR USER ANSWER
  ↓
[2] Describe Requirements
  ↓ ⏸️ MANDATORY WAIT FOR USER DESCRIPTION
  ↓ (Call MCP tools: get_integration_recommendation, find_api_endpoint, search_integration_guides)
  ↓
[3] Create integration-plan.md → Present to user
  ↓ ⏸️ MANDATORY WAIT FOR USER APPROVAL
  ↓ 🛑 STOP - DO NOT GENERATE CODE
  ↓
[4] Information Collection (6 Questions - ONE AT A TIME)
    Q1: Programming Language → ⏸️ WAIT
    Q2: Code Structure → ⏸️ WAIT
    Q3: Credential Handling → ⏸️ WAIT
    Q4: Features → ⏸️ WAIT
    Q5: Environment → ⏸️ WAIT
    Q6: Custom Requirements → ⏸️ WAIT
  ↓ 🛑 STOP - DO NOT GENERATE CODE YET
  ↓
[5] "Ready to generate code?" 
  ↓ ⏸️ MANDATORY WAIT FOR USER "YES"
  ↓ 🛑 FINAL STOP - VERIFY USER SAID "YES"
  ↓
[6] ✅ NOW GENERATE CODE → Deliver files
  ↓
🎉 END - SUCCESS
```

**KEY:**
- 🚨 = Critical action point
- ⏸️ = Mandatory pause - wait for user
- 🛑 = Stop sign - do not proceed
- ✅ = Authorization granted

---

## Example Session

**Agent:** Which language would you like to use for our conversation? 1) English 2) Chinese (中文)
**User:** 1

**Agent:** Please describe what you want to build with PayerMax APIs
**User:** I need card payment and refund for my e-commerce site

**Agent:** *Creates integration-plan.md*
I've created an integration plan with 6 API endpoints. Please review the plan. Reply with: 1) Approve 2) Request changes
**User:** 1

**Agent:** Which programming language? 1) Python 2) Node.js...
**User:** 2

**Agent:** What code structure? 1) Class-based 2) Standalone...
**User:** 3

**Agent:** How to handle credentials? 1) Placeholders 2) Actual...
**User:** 3

**Agent:** Which features? 1) Error handling 2) Logging...
**User:** 1,2,3

**Agent:** Which environment? 1) UAT 2) Production
**User:** 1

**Agent:** Any special requirements? 1) No special requirements 2) Yes - I'll describe them
**User:** 1

**Agent:** All information collected! Ready to generate code? 1) Yes - start generating code 2) No - I need to make changes
**User:** 1

**Agent:** *Generates 8 files: config, 6 endpoints, README*

---

## File Structure Generated

### API Endpoint Files
- `config.js` - Configuration
- `payment_create.js` - Payment creation
- `payment_query.js` - Payment query
- `payment_notification.js` - Payment webhook
- `refund_request.js` - Refund request
- `refund_query.js` - Refund query
- `refund_notification.js` - Refund webhook
- `payermax_client.js` - Main module

### Web Integration Files (Cashier/Drop-in)
- `frontend_integration.html` - Frontend page
- `backend_api.js` - Backend server

### Documentation
- `README.md` - Usage instructions

---

## Troubleshooting

### Issue: Agent Generated Code Without Plan
**Solution:** Agent MUST create plan first. Stop and request: "Please create the integration plan first"

### Issue: Agent Skipped Information Collection
**Solution:** Agent MUST ask all 6 questions in Step 4. This is mandatory.

### Issue: Agent Asked Custom Questions
**Solution:** Agent should only ask the standardized questions with numbered options (1, 2, 3, etc.).

### Issue: Agent Combined Multiple Questions
**Solution:** Agent must ask ONE question at a time and wait for user answer before proceeding.

### Issue: Missing Frontend/Backend Files
**Solution:** For Cashier/Drop-in modes, agent must generate frontend HTML and backend API files.

### Issue: User Provides Text Instead of Number
**Solution:** Agent should accept both numbered responses (1, 2, 3) and text responses ("yes", "Python", etc.) for flexibility.

---

## Integration Checklist

### Before Testing
- [ ] Register at PayerMax Developer Center
- [ ] Obtain test credentials (merchantNo, appId)
- [ ] Generate RSA key pair
- [ ] Upload public key
- [ ] Configure callback URLs
- [ ] Enable payment methods

### Testing
- [ ] Test successful transaction
- [ ] Test failed transaction
- [ ] Verify callbacks work
- [ ] Test error handling

### Production
- [ ] Get production credentials
- [ ] Upload production public key
- [ ] Update to production URLs
- [ ] Configure production callbacks
- [ ] Test in production

For detailed setup, refer to PayerMax Developer Center documentation.
