from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Numeric, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from utility import get_unix_ts, get_unix_ts_2
import re

Base = declarative_base()

class Transaction (Base):
    # https://api.blockcypher.com/v1/eth/main/txs (ok)
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key = True)
    hash = Column(String(64), unique = True)
    received = Column(Integer, nullable = False)
    gas_limit = Column(Integer, nullable = True)
    gas_price = Column(Numeric, nullable = True)
    fees = Column(Integer, nullable = True)
    double_spend = Column(Boolean, nullable = True)
    gas_used = Column(Integer, nullable = True)
    bck_id = Column(Integer, ForeignKey('block.bck_id'), nullable = True)

    # For passing position arguments to the creation of the Transaction object
    def __init__(self, hash, ts, gas_limit, gas_price, fees, double_spend):
        self.hash = hash
        self.received = get_unix_ts(ts)
        self.gas_limit = gas_limit
        self.gas_price = gas_price
        self.fees = fees
        self.double_spend = double_spend

class Block (Base):
    # https://api.blockcypher.com/v1/eth/main/blocks/7
    __tablename__ = 'block'
    bck_id = Column(Integer, primary_key = True)
    bck_time = Column(Integer, nullable = False)
    bck_hash = Column(String(64), nullable = False, unique = True)
    bcl_prev_block = Column(String(64), nullable = True, unique = True)
    bck_size = Column(Integer, nullable = True)
    bck_fees = Column(Integer, nullable = True)
    bkc_total = Column(Integer, nullable = True)
    bck_n_tx = Column(Integer, nullable = True)
    bck_reward = Column(Integer, nullable = True)

    # For passing position arguments to the creation of the Transaction object
    def __init__(self, height, time, hash, prev_block, size, fees, total, n_tx):
        self.bck_id = height
        self.bck_time = get_unix_ts(time)
        self.bck_hash = hash
        self.bck_prev_block = prev_block
        self.bck_size = size
        self.bck_fees = fees
        self.bck_total = total
        self.bck_n_tx = n_tx

class NetworkStats (Base):
    # https://aqats
    __tablename__ = 'networkstats'
    id = Column(Integer, primary_key = True)
    time = Column(Integer, nullable = False, unique = True)
    blockTime = Column(Numeric, nullable = False)
    difficulty = Column(Integer, nullable = False)
    hashrate = Column(Integer, nullable = False)
    usd = Column(Numeric, nullable = True)
    btc = Column(Numeric, nullable = True)

    # For passing position arguments to the creation of the Transaction object
    def __init__(self, time, blockTime, difficulty, hashrate, usd, btc):
        self.time = time
        self.blockTime = blockTime
        self.difficulty = difficulty
        self.hashrate = hashrate
        self.usd = usd
        self.btc = btc

class PoolsStats (Base):
    # https://api.ethpool.org/poolStats
    __tablename__ = 'poolstats'
    id = Column(Integer, primary_key = True)
    file_timestamp = Column(Integer, nullable = False)
    hashRate = Column(Numeric, nullable = False)
    miners =  Column(Integer, nullable = False)
    workers = Column(Integer, nullable = False)
    blocksPerHour = Column(Numeric, nullable = False)

    # For passing position arguments to the creation of the Transaction object
    def __init__(self, time, hashRate, miners, workers, blocksPerHour):
        self.file_timestamp = time
        self.hashRate = hashRate
        self.miners = miners
        self.workers = workers
        self.blocksPerHour = blocksPerHour

class MemoryPool(Base):
    # https://api.blockcypher.com/v1/eth/main
    __tablename__ = 'memoryPool'
    id = Column(Integer, primary_key = True)
    height = Column(Integer, nullable = False)
    time = Column(Integer, nullable = False)
    unconfirmed_count = Column(Integer, nullable = False)
    high_gas_price = Column(Integer, nullable = False)
    medium_gas_price = Column(Integer, nullable = False)
    low_gas_price = Column(Integer, nullable = False)
    last_fork_height = Column(Integer, nullable = False)
    peer_count = Column(Integer, nullable = False)

    # For passing position arguments to the creation of the Transaction object
    def __init__(self, height, time, unc_count, h_gprice, m_gprice, l_gprice, lfork, pcount):
        self.height = height
        self.time = get_unix_ts(time)
        self.unconfirmed_count = unc_count
        self.high_gas_price = h_gprice
        self.medium_gas_price = m_gprice
        self.low_gas_price = l_gprice
        self.last_fork_height = lfork
        self.peer_count = pcount

class EtherGasStation (Base):
    # https://ethgasstation.info/json/ethgasAPI.json (ok)
    __tablename__ = 'ethergasstation'
    egs_id = Column(Integer, primary_key = True)
    egs_ts = Column(Integer, nullable = False)
    average = Column(Numeric, nullable = True)
    fastestWait = Column(Numeric, nullable = True)
    fastWait = Column(Numeric, nullable = True)
    egs_fast = Column(Numeric, nullable = True)
    safeLowWait = Column(Numeric, nullable = True)
    blockNum = Column(Numeric, nullable = True)
    avgWait = Column(Numeric, nullable = True)
    block_time = Column(Numeric, nullable = True)
    speed = Column(Numeric, nullable = True)
    egs_fastest = Column(Numeric, nullable = True)
    egs_safeLow = Column(Numeric, nullable = True)

class GasOracleEthChain (Base):
    # https://www.etherchain.org/api/gasPriceOracle (ok)
    # https://www.etherchain.org/tools/gasPriceOracle
    __tablename__ = 'gasoracleethchain'
    id = Column(Integer, primary_key = True)
    file_timestamp = Column(Integer, nullable = False, unique = True)
    safeLow = Column(Numeric, nullable = True)
    standard = Column(Numeric, nullable = True)
    fast = Column(Numeric, nullable = True)
    fastest = Column(Numeric, nullable = True)

    def __init__(self, ts, safeLow, standard, fast, fastest):
        self.file_timestamp = ts
        self.safeLow = safeLow
        self.standard = standard
        self.fast = fast
        self.fastest = fastest

class PendingTransactionFound(Base):
    # https://etherscan.io/txsPending
    __tablename__ = 'pendingtxsfound'
    id = Column(Integer, primary_key = True)
    ts = Column(Integer, nullable = False)
    pending_txs_found = Column(Integer, nullable = False)

    def __init__(self, ts, pending_txs_found):
        self.ts = get_unix_ts_2(ts) # '%m/%d/%Y %I:%M:%S %p'
        self.pending_txs_found = pending_txs_found

if __name__ == '__main__':
    engine = create_engine('sqlite:///tx.db')
    Session = sessionmaker(bind = engine)
    Base.metadata.create_all(engine)
