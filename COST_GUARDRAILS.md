# COST GUARDRAILS - Bautomate Project

## 🚨 STOP BONCOS - MUST DO

### 1. Budget Alerts (Wajib Sekarang!)
```
Portal Azure → Cost Management → Budgets → Create Budget
- Amount: $100 (student limit)
- Alert 1: $50 (50%)
- Alert 2: $75 (75%)
- Alert 3: $90 (90%)
```

### 2. Synapse Spark Pool Auto-Pause
```
Synapse Workspace → Manage → Apache Spark pools → <pool-name>
→ Auto-pause: 15 minutes
→ Auto-shutdown: 20 minutes
```

### 3. Quick Wins Cost Control

| Action | Impact |
|--------|--------|
| Delete unused Spark pools | -$50-200/month |
| Use Serverless SQL (not provisioned) | Pay per query only |
| Blob Storage Cool tier for old data | -30% storage cost |
| Enable Cost Alerts | Prevent surprise bills |

### 4. Monitoring Commands
```bash
# Cek biaya harian
az consumption usage list --start-date 2026-09-01 --output table

# Cek budget alerts
az consumption budget list --output table

# Cek resource group costs
az cost management query --from-date 2026-09-01 --granularity Daily --output table
```

### 5. Emergency Stop
```bash
# Hapus semua Spark pools kalau boncos parah
az synapse spark pool delete --name <pool-name> --workspace-name <workspace>

# Delete resource group (NUCLEUS DROP)
az group delete --name <resource-group> --yes --no-wait
```

## Checklist

- [ ] Budget alert di $50 dan $75
- [ ] Synapse auto-pause 15 menit
- [ ] Setup cost monitoring dashboard
- [ ] Hapus Spark pool kalau tidak dipakai
- [ ] Catat semua resource yang dibuat
