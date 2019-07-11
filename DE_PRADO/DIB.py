class DIB:
    def __init__(self, file_path,
                 len_init=1,
                 _window = 20,
                 unit='D',
                 index_date='date',
                 col_price ='close',
                 col_volume='volume'):
        self.window = _window
        # init 값을 설정을 위한 bar의 수
        self.len_init = _len_init
        
        ### input ###
        self.data = pd.read_csv(file_path,index_col=index_date)
        self.data.index = pd.to_datetime(self.data.index)
        self.data.index.names = ['timestamp']
        # unit 단위로 list 화
        self.data = [g for n, g in self.data.groupby(pd.Grouper(level='timestamp', freq=unit))]
        
        self.exp_num_ticks = self.exp_num_ticks_init
        self.arr_T = []
        self.arr_b = []
        ### output ###
        self.dollar = pd.DataFrame(columns=['close']) 
        self.dollar.index.names = ['timestamp']
        
    def ewma(self):
        
    def init(self):
        
    def process(self):
        
    def getDF(self):
        return self.dollar
        