"""Read Skyrim PEX header strings, retaining executable tables byte for byte."""
import struct


def metadata(data):
    if len(data)<16 or data[:4]!=bytes.fromhex('fa57c0de') or data[4:8]!=bytes.fromhex('03020001'):
        raise ValueError('Unsupported Skyrim PEX header')
    pos=16;values={}
    for name in ('source','user','computer'):
        if pos+2>len(data):raise ValueError('Truncated PEX header')
        n=struct.unpack_from('>H',data,pos)[0];pos+=2
        if pos+n>len(data):raise ValueError('Truncated PEX metadata')
        values[name]=data[pos:pos+n].decode('utf-8');pos+=n
    if pos>=len(data):raise ValueError('Missing PEX tables')
    return values,pos


def anonymize(data):
    values,end=metadata(data)
    def encoded(value):
        b=value.encode('utf-8');return struct.pack('>H',len(b))+b
    clean=data[:16]+encoded(values['source'])+encoded('AstraAsedio')+encoded('Build')+data[end:]
    after,new_end=metadata(clean)
    assert after['source']==values['source'] and clean[new_end:]==data[end:]
    return clean
