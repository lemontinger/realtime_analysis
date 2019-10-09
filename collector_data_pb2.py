# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='collector_data.proto',
  package='',
  serialized_pb='\n\x14\x63ollector_data.proto\"s\n\nSearchInfo\x12\x0e\n\x06\x61\x64_num\x18\x01 \x01(\r\x12\x12\n\nfilter_num\x18\x02 \x01(\r\x12\x12\n\nchange_num\x18\x03 \x01(\r\x12\x0c\n\x04pvid\x18\x04 \x01(\t\x12\x1f\n\x07rl_info\x18\x05 \x03(\x0b\x32\x0e.ReachLineInfo\"\x85\x03\n\rUpdateMsgInfo\x12\r\n\x05msgid\x18\x01 \x02(\x04\x12\x12\n\nbudgettype\x18\x02 \x02(\r\x12\x0e\n\x06userid\x18\x03 \x01(\x04\x12\x0e\n\x06planid\x18\x04 \x01(\x04\x12\x13\n\x0buserbalance\x18\x05 \x01(\x02\x12\x12\n\nuserbudget\x18\x06 \x01(\x02\x12\x10\n\x08usercost\x18\x07 \x01(\x02\x12\x12\n\nplanbudget\x18\x08 \x01(\x02\x12\x10\n\x08plancost\x18\t \x01(\x02\x12\r\n\x05query\x18\n \x01(\x0c\x12\x0b\n\x03src\x18\x0b \x01(\x0c\x12\x0f\n\x07keyword\x18\x0c \x01(\x0c\x12\x12\n\nclickprice\x18\r \x01(\x02\x12\x11\n\tmatchtype\x18\x0e \x01(\x05\x12\x12\n\nchargetime\x18\x0f \x01(\x04\x12\x0c\n\x04lsid\x18\x10 \x01(\x04\x12\x11\n\tclicktime\x18\x11 \x01(\r\x12\x10\n\x08\x64\x65\x61ltime\x18\x12 \x01(\r\x12\x10\n\x08gspprice\x18\x13 \x01(\x02\x12\x11\n\tbucket_id\x18\x14 \x01(\r\x12\x10\n\x08\x62idprice\x18\x15 \x01(\x02\"t\n\rCollectorData\x12\x0e\n\x06tv_sec\x18\x01 \x02(\x04\x12\x0f\n\x07tv_usec\x18\x02 \x02(\x04\x12 \n\x0bsearch_info\x18\x03 \x01(\x0b\x32\x0b.SearchInfo\x12 \n\x08msg_info\x18\x04 \x01(\x0b\x32\x0e.UpdateMsgInfo\"\xf1\x01\n\rReachLineInfo\x12\r\n\x05\x61\x64_id\x18\x01 \x01(\r\x12\x15\n\rad_account_id\x18\x02 \x01(\x04\x12\x12\n\nad_plan_id\x18\x03 \x01(\r\x12\x13\n\x0b\x61\x64_bidprice\x18\x04 \x01(\x01\x12\x12\n\nad_quality\x18\x05 \x01(\x02\x12\x14\n\x0c\x61\x64_rank_pctr\x18\x06 \x01(\x01\x12\x11\n\tpush_left\x18\x07 \x01(\r\x12\x0c\n\x04ppad\x18\x08 \x01(\x08\x12\x0f\n\x07is_show\x18\t \x01(\x08\x12\x16\n\x0e\x61\x64_final_price\x18\n \x01(\x01\x12\x1d\n\x06reason\x18\x0b \x01(\x0e\x32\r.ThresholdErr*`\n\nBudgetType\x12\x0b\n\x07\x43ONSUME\x10\x01\x12\x0c\n\x08RECHARGE\x10\x02\x12\x11\n\rMODIFY_BUDGET\x10\x03\x12\r\n\tANTI_SPAM\x10\x04\x12\x08\n\x04\x43OST\x10\x05\x12\x0b\n\x07\x42\x41LANCE\x10\x06*\xe4\x01\n\x0cThresholdErr\x12\x1f\n\x1b\x41\x43\x43OUNT_BALANCE_LINE_HIDDEN\x10\x64\x12\x18\n\x14\x41\x43\x43OUNT_BALANCE_LINE\x10\x65\x12\x1e\n\x1a\x41\x43\x43OUNT_BUDGET_LINE_HIDDEN\x10g\x12\x17\n\x13\x41\x43\x43OUNT_BUDGET_LINE\x10h\x12\x1b\n\x17PLAN_BUDGET_LINE_HIDDEN\x10i\x12\x14\n\x10PLAN_BUDGET_LINE\x10j\x12\x17\n\x13PRICE_LOW_THRESHOLD\x10k\x12\x14\n\x0fREACH_LINE_INIT\x10\xd0\x0f')

_BUDGETTYPE = descriptor.EnumDescriptor(
  name='BudgetType',
  full_name='BudgetType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='CONSUME', index=0, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='RECHARGE', index=1, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='MODIFY_BUDGET', index=2, number=3,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ANTI_SPAM', index=3, number=4,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='COST', index=4, number=5,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='BALANCE', index=5, number=6,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=895,
  serialized_end=991,
)


_THRESHOLDERR = descriptor.EnumDescriptor(
  name='ThresholdErr',
  full_name='ThresholdErr',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='ACCOUNT_BALANCE_LINE_HIDDEN', index=0, number=100,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ACCOUNT_BALANCE_LINE', index=1, number=101,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ACCOUNT_BUDGET_LINE_HIDDEN', index=2, number=103,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ACCOUNT_BUDGET_LINE', index=3, number=104,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='PLAN_BUDGET_LINE_HIDDEN', index=4, number=105,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='PLAN_BUDGET_LINE', index=5, number=106,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='PRICE_LOW_THRESHOLD', index=6, number=107,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='REACH_LINE_INIT', index=7, number=2000,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=994,
  serialized_end=1222,
)


CONSUME = 1
RECHARGE = 2
MODIFY_BUDGET = 3
ANTI_SPAM = 4
COST = 5
BALANCE = 6
ACCOUNT_BALANCE_LINE_HIDDEN = 100
ACCOUNT_BALANCE_LINE = 101
ACCOUNT_BUDGET_LINE_HIDDEN = 103
ACCOUNT_BUDGET_LINE = 104
PLAN_BUDGET_LINE_HIDDEN = 105
PLAN_BUDGET_LINE = 106
PRICE_LOW_THRESHOLD = 107
REACH_LINE_INIT = 2000



_SEARCHINFO = descriptor.Descriptor(
  name='SearchInfo',
  full_name='SearchInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='ad_num', full_name='SearchInfo.ad_num', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='filter_num', full_name='SearchInfo.filter_num', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='change_num', full_name='SearchInfo.change_num', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='pvid', full_name='SearchInfo.pvid', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='rl_info', full_name='SearchInfo.rl_info', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=24,
  serialized_end=139,
)


_UPDATEMSGINFO = descriptor.Descriptor(
  name='UpdateMsgInfo',
  full_name='UpdateMsgInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='msgid', full_name='UpdateMsgInfo.msgid', index=0,
      number=1, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='budgettype', full_name='UpdateMsgInfo.budgettype', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='userid', full_name='UpdateMsgInfo.userid', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='planid', full_name='UpdateMsgInfo.planid', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='userbalance', full_name='UpdateMsgInfo.userbalance', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='userbudget', full_name='UpdateMsgInfo.userbudget', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='usercost', full_name='UpdateMsgInfo.usercost', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='planbudget', full_name='UpdateMsgInfo.planbudget', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='plancost', full_name='UpdateMsgInfo.plancost', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='query', full_name='UpdateMsgInfo.query', index=9,
      number=10, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='src', full_name='UpdateMsgInfo.src', index=10,
      number=11, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='keyword', full_name='UpdateMsgInfo.keyword', index=11,
      number=12, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='clickprice', full_name='UpdateMsgInfo.clickprice', index=12,
      number=13, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='matchtype', full_name='UpdateMsgInfo.matchtype', index=13,
      number=14, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='chargetime', full_name='UpdateMsgInfo.chargetime', index=14,
      number=15, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='lsid', full_name='UpdateMsgInfo.lsid', index=15,
      number=16, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='clicktime', full_name='UpdateMsgInfo.clicktime', index=16,
      number=17, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='dealtime', full_name='UpdateMsgInfo.dealtime', index=17,
      number=18, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='gspprice', full_name='UpdateMsgInfo.gspprice', index=18,
      number=19, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='bucket_id', full_name='UpdateMsgInfo.bucket_id', index=19,
      number=20, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='bidprice', full_name='UpdateMsgInfo.bidprice', index=20,
      number=21, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=142,
  serialized_end=531,
)


_COLLECTORDATA = descriptor.Descriptor(
  name='CollectorData',
  full_name='CollectorData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='tv_sec', full_name='CollectorData.tv_sec', index=0,
      number=1, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='tv_usec', full_name='CollectorData.tv_usec', index=1,
      number=2, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='search_info', full_name='CollectorData.search_info', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='msg_info', full_name='CollectorData.msg_info', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=533,
  serialized_end=649,
)


_REACHLINEINFO = descriptor.Descriptor(
  name='ReachLineInfo',
  full_name='ReachLineInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='ad_id', full_name='ReachLineInfo.ad_id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='ad_account_id', full_name='ReachLineInfo.ad_account_id', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='ad_plan_id', full_name='ReachLineInfo.ad_plan_id', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='ad_bidprice', full_name='ReachLineInfo.ad_bidprice', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='ad_quality', full_name='ReachLineInfo.ad_quality', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='ad_rank_pctr', full_name='ReachLineInfo.ad_rank_pctr', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='push_left', full_name='ReachLineInfo.push_left', index=6,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='ppad', full_name='ReachLineInfo.ppad', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='is_show', full_name='ReachLineInfo.is_show', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='ad_final_price', full_name='ReachLineInfo.ad_final_price', index=9,
      number=10, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='reason', full_name='ReachLineInfo.reason', index=10,
      number=11, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=100,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=652,
  serialized_end=893,
)

_SEARCHINFO.fields_by_name['rl_info'].message_type = _REACHLINEINFO
_COLLECTORDATA.fields_by_name['search_info'].message_type = _SEARCHINFO
_COLLECTORDATA.fields_by_name['msg_info'].message_type = _UPDATEMSGINFO
_REACHLINEINFO.fields_by_name['reason'].enum_type = _THRESHOLDERR
DESCRIPTOR.message_types_by_name['SearchInfo'] = _SEARCHINFO
DESCRIPTOR.message_types_by_name['UpdateMsgInfo'] = _UPDATEMSGINFO
DESCRIPTOR.message_types_by_name['CollectorData'] = _COLLECTORDATA
DESCRIPTOR.message_types_by_name['ReachLineInfo'] = _REACHLINEINFO

class SearchInfo(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SEARCHINFO
  
  # @@protoc_insertion_point(class_scope:SearchInfo)

class UpdateMsgInfo(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _UPDATEMSGINFO
  
  # @@protoc_insertion_point(class_scope:UpdateMsgInfo)

class CollectorData(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _COLLECTORDATA
  
  # @@protoc_insertion_point(class_scope:CollectorData)

class ReachLineInfo(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REACHLINEINFO
  
  # @@protoc_insertion_point(class_scope:ReachLineInfo)

# @@protoc_insertion_point(module_scope)
