#!/bin/bash
export SOLANA_METRICS_CONFIG="host=https://metrics.solana.com:8086,db=mainnet-beta,u=mainnet-beta_write,p=password"
/mnt/solana/target/release/solana-validator --identity /home/ubuntu/.clock/clock-id.json --rpc-port 8899 --entrypoint entrypoint.mainnet-beta.solana.com:8001 --limit-ledger-size --log /mnt/logs/solana-validator.log --accounts /mnt/solana-accounts --ledger /mnt/solana-ledger --snapshots /mnt/solana-snapshots --vote-account /home/ubuntu/.clock/clock-vote.json --no-snapshot-fetch --geyser-plugin-config /home/ubuntu/accountsconfig.json
