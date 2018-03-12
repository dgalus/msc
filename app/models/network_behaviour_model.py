class NetworkBehaviourModel:
    def __init__(self, sessions_count, diff_syn_ack, l2_traffic, l3_traffic, l4_traffic):
        self.sessions_count = sessions_count
        self.diff_syn_ack = diff_syn_ack
        self.l2_traffic = l2_traffic
        self.l3_traffic = l3_traffic
        self.l4_traffic = l4_traffic