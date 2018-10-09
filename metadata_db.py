from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Numeric, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import re

Base = declarative_base()

class Transaction (Base):
    # https://api.blockcypher.com/v1/eth/main/txs (ok)
    __tablename__ = 'transaction'
    tx_id = Column(Integer, primary_key = True)
    tx_received = Column(Integer, nullable = False)
    tx_hash = Column(String(64), unique = True)
    tx_gas_limit = Column(Integer, nullable = True)
    tx_gas_price = Column(Numeric, nullable = True)
    tx_fees = Column(Integer, nullable = True)
    tx_double_spend = Column(Boolean, nullable = True)
    bck_id = Column(Integer, ForeignKey('block.bck_id'), nullable = True)

    # For passing position arguments to the creation of the Transaction object
    def __init__(self, ts, hash, gas_limit, gas_price, fees, double_spend):
        self.tx_received = self._get_unix_ts(ts)
        self.tx_hash = hash
        self.tx_gas_limit = gas_limit
        self.tx_gas_price = gas_price
        self.tx_fees = fees
        self.tx_double_spend = double_spend

    def _get_unix_ts(self, ts):
        print(ts)
        ts = re.sub('.\d{1,}Z', '', ts)
        format = '%Y-%m-%dT%H:%M:%S'
        return int(datetime.strptime(ts, format).strftime('%s'))

class Block (Base):
    # https://api.blockcypher.com/v1/eth/main/blocks/7
    __tablename__ = 'block'
    bck_id = Column(Integer, primary_key = True)
    bck_ts = Column(Integer, nullable = False)
    bck_hash = Column(String(64), nullable = False, unique = True)
    bck_gas_limit = Column(Integer, nullable = True)
    bck_time = Column(Integer, nullable = True)
    reward = Column(Numeric, nullable = True)
    fees = Column(Numeric, nullable = True)

class NetworkStats (Base):
    # https://api.ethpool.org/networkStats
    __tablename__ = 'networkstats'
    ns_id = Column(Integer, primary_key = True)
    ns_ts = Column(Integer, nullable = False)
    difficulty = Column(Integer, nullable = False)
    ns_hashrate = Column(Numeric, nullable = False)
    usd = Column(Numeric, nullable = True)
    btc = Column(Numeric, nullable = True)

class PoolStats (Base):
    # https://api.ethpool.org/poolStats
    __tablename__ = 'poolstats'
    ps_id = Column(Integer, primary_key = True)
    ps_ts = Column(Integer, nullable = False)
    ps_hashrate = Column(Numeric, nullable = False)
    miners =  Column(Integer, nullable = False)
    workers = Column(Integer, nullable = False)
    blocksPerHour = Column(Numeric, nullable = False)

class BlockCypherPoolStats(Base):
    # https://api.blockcypher.com/v1/eth/main
    __tablename__ = 'blockcypherpoolstats'
    bcps_id = Column(Integer, primary_key = True)
    bcps_ts = Column(Integer, nullable = False)

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

class EtherChain (Base):
    # https://www.etherchain.org/api/gasPriceOracle (ok)
    # https://www.etherchain.org/tools/gasPriceOracle
    __tablename__ = 'etherchain'
    ec_id = Column(Integer, primary_key = True)
    ec_ts = Column(Integer, nullable = False)
    ec_safeLow = Column(Numeric, nullable = True)
    standard = Column(Numeric, nullable = True)
    ec_fast = Column(Numeric, nullable = True)
    ec_fastest = Column(Numeric, nullable = True)

if __name__ == '__main__':
    engine = create_engine('sqlite:///tx.db')
    Session = sessionmaker(bind = engine)
    Base.metadata.create_all(engine)
