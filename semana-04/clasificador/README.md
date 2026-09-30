# Message Classifier — Credit/Debit Card Customer Support (US)

## Domain
Messages customers send to the support team of a credit/debit card issuer in the United States.

## Fields and allowed values

### Category 
- lost_stolen_card
- charge_dispute
- account_locked
- account_reactivation
- general_inquiry

### Sentiment
- positive
- neutral
- negative

### Priority
- high — money is at risk right now, or the customer cannot access
  their funds
- medium — real problem, no immediate urgency
- low — informational question

### Summary
One sentence, 15 words max.

## Data rule
Never full card numbers, SSNs or any other possible real private data. Last 4 digits only.