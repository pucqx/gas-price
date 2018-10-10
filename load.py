from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from metadata_db import Base, Transaction
from extract_from_file import Extract_from_file
from extract_block import Extract_block

class Load:

    def __init__(self, db_name = 'tx.db'):
        self.db_name = db_name
        self._set_session()

    def _load_tx(self, args):
        if not self.session.query(Transaction).filter_by(tx_hash = args[1]).first():
            tx = Transaction(*args)
            self.session.merge(tx)
            self.session.commit()

    def _load_bckId_gasUsed_into_tx(self, args):
        tx = self.session.query(Transaction).filter_by(tx_hash = args['hash']).first()
        print(hash)
        tx.bck_id = args['block_height']
        tx.tx_gas_used = args['gas_used']
        self.session.commit()

    def _set_session(self):
        engine = create_engine('///'.join(['sqlite:', self.db_name]))
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind = engine)
        self.session = DBSession()

    def load_txs(self, txs):
        for tx in txs: self._load_tx(tx)

    def load_bckId_gasUsed_into_txs(self):
        extract_block = Extract_block()
        hashes = extract_block.get_hashes_without_block_id()
        for hash in hashes:
            print(hash)
            bckId_gasUsed = extract_block.get_bckId_gasUsed(hash)
            if bckId_gasUsed:
                print('bckId_gasUsed: ', bckId_gasUsed)
                self._load_bckId_gasUsed_into_tx(bckId_gasUsed)

if __name__ == '__main__':
    load = Load('tx.db')
    # extract = Extract_from_file()
    # load.load_txs(extract.get_txs())
    load.load_bckId_gasUsed_into_txs()
