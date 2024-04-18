"""This is a python script for health check of devices"""
import re
import os
from prettytable import PrettyTable,ALL

class healthcheck:

    def __init__(self,RSI_filename):
        self.RSI_filename = RSI_filename

    def pvhcu(self,RSI):

        #Color coding
        R = "\033[91m" #RED
        G = "\033[92m" #GREEN
        Y = "\033[93m" #yellow
        B = "\033[94m" #Blue
        N = "\033[0m" #Reset
        self.RSI = RSI
        
        #initialing empty list used to append data later
        dict_rsi = {}
        dict_rsi['re_role'] = []
        dict_rsi['re_mem'] = []
        dict_rsi['re_cpu_user'] = []
        dict_rsi['re_cpu_Background'] = []
        dict_rsi['re_cpu_Kernel'] = []
        dict_rsi['re_cpu_Interrupt'] = []
        dict_rsi['re_cpu_Idle'] = []
        dict_rsi['re_last_reboot_reason'] = []
        dict_rsi['alarm'] = []
        dict_rsi['core'] = []
        dict_rsi['re'] = []
        dict_rsi['fpc'] = []
        dict_rsi['process_nonzero'] = []
        dict_rsi['hw_component'] = []
        dict_rsi['re_refpc_starttime'] = []
        dict_rsi['re_refpc_uptime'] = []
        dict_rsi['fpc_info'] = []
        dict_rsi['fpc_info_slot'] = []
        dict_rsi['fpc_info_temp'] = []
        dict_rsi['fpc_info_cpu_total'] = []
        dict_rsi['fpc_info_cpu_intrp'] = []
        dict_rsi['fpc_info_1min'] = []
        dict_rsi['fpc_info_5min'] = []
        dict_rsi['fpc_info_15min'] = []
        dict_rsi['fpc_info_dram'] = []
        dict_rsi['fpc_info_heap'] = []
        dict_rsi['fpc_info_buf'] = []
        FPC_info_temp = [] #Number of FPC printing helper variable list
        #integer converter definition
        def int_conv(string):
            string = re.findall('\d+',string)
            string = float(string[0])
            return string

        fp = open(RSI,'r')
        lines = fp.readlines()
        for each in lines:
           #print(each) 
           uptime = re.findall('System booted: (.*)[A-Z]{3} \((.*)(ago)\)',each)
           if uptime:
               dict_rsi['uptime'] = uptime[0][1]+'h'
               #print(dict_rsi['uptime'])
               #continue

           Hostname = re.findall('(Hostname:) (.*)',each)
           if Hostname:
               dict_rsi['hostname'] = Hostname[0][1]
               #print(dict_rsi['hostname'])

           Model = re.findall('(^Model:) (.*)',each)
           if Model:
               dict_rsi['model'] = Model[0][1]
               #print(dict_rsi['model'])

           Version = re.findall('Junos: (.*)',each)
           if Version:
               dict_rsi['version'] = Version[0]
               #print(dict_rsi['version'])
           
           host_version = re.findall('JUNOS Host.*platform package \[(.*)\]',each)
           if host_version:
               dict_rsi['host_version'] = host_version[0]
               #print(dict_rsi['host_version'])

           core = re.findall('.*\.core\.[0-9]*\.[t]*gz.*|.*\.core-tarball\.[0-9]*\.tgz.*|.*crashinfo\.[0-9]*\.tgz|.*\.[0-9]*\.core\.[t]*gz|.*vmcore.*',each)
           if core:
               dict_rsi['core'].append(core[0])
               #print(dict_rsi['core'])

           Alarm = re.findall('^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}.*Minor.*|^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}.*Major.*',each)
           if Alarm:
               dict_rsi['alarm'].append(Alarm[0])
               #print(dict_rsi['alarm'])

           RE = re.findall('Routing Engine [01].*(RE-.*)|Routing Engine [01].*(EX.*)',each)
           if RE:
               RE[0] = list(RE[0])
               while ('' in RE[0]):
                   RE[0].remove('')
               dict_rsi['re'].append(RE[0])

           FPC = re.findall('(FPC [0-9][0-9]*).*REV',each)
           if FPC:
               dict_rsi['fpc'].append(FPC[0])
           
           FPC_info = re.findall('([0-9][0-9]*)  Online\ *([0-9][0-9])\ *(\d*)\ *(\d*)\ *(\d*)\ *(\d*)\ *(\d*)\ *(\d*)\ *(\d*)\ *(\d*)\ *(\d*)\ *',each)
           if FPC_info:
               FPC_info[0] = list(FPC_info[0])
               while ('' in FPC_info[0]):
                   FPC_info[0].remove('')
               FPC_info_temp = FPC_info[0]  
               if len(FPC_info[0]) == 10:    
                   dict_rsi['fpc_info'].append(FPC_info[0][0])
                   dict_rsi['fpc_info_slot'].append(FPC_info[0][0])
                   dict_rsi['fpc_info_temp'].append(FPC_info[0][1]+' Celcius')
                   dict_rsi['fpc_info_cpu_total'].append(FPC_info[0][2]+'%')
                   dict_rsi['fpc_info_cpu_intrp'].append(FPC_info[0][3]+'%')
                   dict_rsi['fpc_info_1min'].append(FPC_info[0][4]+'%')
                   dict_rsi['fpc_info_5min'].append(FPC_info[0][5]+'%')
                   dict_rsi['fpc_info_15min'].append(FPC_info[0][6]+'%')
                   dict_rsi['fpc_info_dram'].append(FPC_info[0][7]+'MB')
                   dict_rsi['fpc_info_heap'].append(FPC_info[0][8]+'%')
                   dict_rsi['fpc_info_buf'].append(FPC_info[0][9]+'%')
                   #print(dict_rsi['fpc_info'])
           
           #Active = re.findall('[0-9]{1,4}M Active',each)
           #if Active:
           #    print(Active[0])

           #Inact = re.findall('[0-9]{1,4}M Inact',each)
           #if Inact:
           #    print(Inact[0])

           #wired = re.findall('[0-9]{1,4}M Wired',each)
           #if wired:
           #    print(wired[0])

           #buf = re.findall('[0-9]{1,4}M Buf',each)
           #if buf:
           #    print(buf[0])

           mem = re.findall('Mem: ([0-9]{1,4}[M|G|K]) Active, ([0-9]{1,4}[M|G|K]) Inact, ([0-9]{1,4}[M|G|K]) Wired, ([0-9]{1,4}[M|G|K]) Buf, ([0-9]{1,4}[M|G|K]) Free|Mem: ([0-9]{1,4}[M|G|K]) Active, ([0-9]{1,4}[M|G|K]) Inact, ([0-9]{1,4}[M|G|K]) Wired, ([0-9]{1,4}[M|G|K]) Cache, ([0-9]{1,4}[M|G|K]) Buf, ([0-9]{1,4}[M|G|K]) Free',each)
           if mem:
               dict_rsi['mem'] = mem[0]
               dict_rsi['mem'] = list(dict_rsi['mem'])
               while ('' in dict_rsi['mem']):
                   dict_rsi['mem'].remove('')

           #Match when laundry memory present in the memory usage
           laundry = re.findall('Mem: ([0-9]{1,4}[M|G|K]) Active, ([0-9]{1,4}[M|G|K]) Inact, ([0-9]{1,4}[M|G|K]) Laundry, ([0-9]{1,4}[M|G|K]) Wired, ([0-9]{1,4}[M|G|K]) Buf, ([0-9]{1,4}[M|G|K]) Free',each)
           if laundry:
               dict_rsi['laun'] = laundry[0]
               dict_rsi['laun'] = list(dict_rsi['laun'])
               while ('' in dict_rsi['laun']):
                   dict_rsi['laun'].remove('')


           swap = re.findall('Swap: ([0-9]{1,4}M) Total, ([0-9]{1,4}M) Free|Swap: ([0-9]{1,4}M) Total, ([0-9]{1,4}M) Used, ([0-9]{1,4}M) Free, ([0-9]{1,2}%) Inuse',each)
           if swap:
               swap[0] = list(swap[0])
               #swap[0] = ''.join(swap[0]).split()
               while ('' in swap[0]):
                   swap[0].remove('')
               dict_rsi['swap'] = swap[0]
               #print(dict_rsi['swap'])
               #print(len(swap[0]))

           #process_nonzero = re.findall('root.*(\d{1,3}\.\d{1,2}%.*)',each)
           #process_nonzero = re.findall('root.*\ (0\.0[1-9]%.*|0\.[1-9][0-9]%.*|[1-9][0-9][0-9].[0-9][0-9]%.*|[1-9][0-9].[0-9][0-9]%.*|[1-9].[0-9][0-9]%.*)',each)#all non-zer0 processes
           process_nonzero = re.findall('root.*\ ([1-9][0-9][0-9].[0-9][0-9]%.*|[1-9][0-9].[0-9][0-9]%.*)',each)#double-triple digit cpu utilisation
           if process_nonzero:
               dict_rsi['process_nonzero'].append(process_nonzero[0])
               #print(dict_rsi['process_nonzero'])

           sw_input_cntrl_drops = re.findall('Software input control plane drops  :\ *(\d+)',each)
           if sw_input_cntrl_drops:
               dict_rsi['pfe_sw_input_cntrl_drops'] = sw_input_cntrl_drops[0]
               #print(dict_rsi['pfe_sw_input_cntrl_drops'])
           
           sw_input_high_drops = re.findall('Software input high drops           :\ *(\d+)',each)
           if sw_input_high_drops:
               dict_rsi['pfe_sw_input_high_drops'] = sw_input_high_drops[0]
               #print(dict_rsi['pfe_sw_input_high_drops'])

           sw_input_medium_drops = re.findall('Software input medium drops         :\ *(\d+)',each)
           if sw_input_medium_drops:
               dict_rsi['pfe_sw_input_medium_drops'] = sw_input_medium_drops[0]
               #print(dict_rsi['pfe_sw_input_medium_drops'])
           
           sw_input_low_drops = re.findall('Software input low drops            :\ *(\d+)',each)
           if sw_input_low_drops:
               dict_rsi['pfe_sw_input_low_drops'] = sw_input_low_drops[0]
               #print(dict_rsi['pfe_sw_input_low_drops'])
           
           sw_output_drops = re.findall('Software output drops               :\ *(\d+)',each)
           if sw_output_drops:
               dict_rsi['pfe_sw_output_drops'] = sw_output_drops[0]
               #print(dict_rsi['pfe_sw_output_drops'])

           hw_input_drops = re.findall('Hardware input drops                :\ *(\d+)',each)
           if hw_input_drops:
               dict_rsi['pfe_hw_input_drops'] = hw_input_drops[0]
               #print(dict_rsi['pfe_hw_input_drops'])
           
           pfe_timeout = re.findall('Timeout                    :\ *(\d+)',each)
           if pfe_timeout:
               dict_rsi['pfe_timeout'] = pfe_timeout[0]
               #print(dict_rsi['pfe_timeout'])

           pfe_trun_key = re.findall('Truncated key              :\ *(\d+)',each)
           if pfe_trun_key:
               dict_rsi['pfe_trun_key'] = pfe_trun_key[0]
               #print(dict_rsi['pfe_trun_key'])
           pfe_bits_test = re.findall('Bits to test               :\ *(\d+)',each)
           if pfe_bits_test:
               dict_rsi['pfe_bits_test'] = pfe_bits_test[0]
               #print(dict_rsi['pfe_bits_test'])
           
           pfe_data_err = re.findall('Data error                 :\ *(\d+)',each)
           if pfe_data_err:
               dict_rsi['pfe_data_err'] = pfe_data_err[0]
               #print(dict_rsi['pfe_data_err'])
           
           pfe_tcp_hdr_len_err = re.findall('TCP header length error    :\ *(\d+)',each)
           if pfe_tcp_hdr_len_err:
               dict_rsi['pfe_tcp_hdr_len_err'] = pfe_tcp_hdr_len_err[0]
               #print(dict_rsi['pfe_tcp_hdr_len_err'])
           
           pfe_stk_undr_flow = re.findall('Stack underflow            :\ *(\d+)',each)
           if pfe_stk_undr_flow:
               dict_rsi['pfe_stk_undr_flow'] = pfe_stk_undr_flow[0]
               #print(dict_rsi['pfe_stk_undr_flow'])
           
           pfe_stk_ovr_flow = re.findall('Stack overflow             :\ *(\d+)',each)
           if pfe_stk_ovr_flow:
               dict_rsi['pfe_stk_ovr_flow'] = pfe_stk_ovr_flow[0]
               #print(dict_rsi['pfe_stk_ovr_flow'])
           
           pfe_nrml_discard = re.findall('Normal discard             :\ *(\d+)',each)
           if pfe_nrml_discard:
               dict_rsi['pfe_nrml_discard'] = pfe_nrml_discard[0]
               #print(dict_rsi['pfe_nrml_discard'])
           
           pfe_ext_discard = re.findall('Extended discard           :\ *(\d+)',each)
           if pfe_ext_discard:
               dict_rsi['pfe_ext_discard'] = pfe_ext_discard[0]
               #print(dict_rsi['pfe_ext_discard'])
           
           pfe_inv_int = re.findall('Invalid interface          :\ *(\d+)',each)
           if pfe_inv_int:
               dict_rsi['pfe_inv_int'] = pfe_inv_int[0]
               #print(dict_rsi['pfe_inv_int'])
           
           pfe_info_cell_drop = re.findall('Info cell drops            :\ *(\d+)',each)
           if pfe_info_cell_drop:
               dict_rsi['pfe_info_cell_drop'] = pfe_info_cell_drop[0]
               #print(dict_rsi['pfe_info_cell_drop'])
           
           pfe_fab_drop = re.findall('Fabric drops               :\ *(\d+)',each)
           if pfe_fab_drop:
               dict_rsi['pfe_fab_drop'] = pfe_fab_drop[0]
               #print(dict_rsi['pfe_fab_drop'])

           re_role = re.findall('^\ *Current state\ *([a-z|A-Z]+)',each)
           if re_role:
               dict_rsi['re_role'].append(re_role[0])
               #print(dict_rsi['re_role'])
           
           re_mem = re.findall('Memory utilization\ *(\d+.*)',each)
           if re_mem:
               dict_rsi['re_mem'].append(re_mem[0])
               #print(dict_rsi['re_mem'])
           
           re_cpu_user = re.findall('User\ *(\d+)',each)
           if re_cpu_user:
               dict_rsi['re_cpu_user'].append(re_cpu_user[0]+'%')
               #print(dict_rsi['re_cpu_user'])
          
           re_cpu_Background = re.findall('Background\ *(\d+)',each)
           if re_cpu_Background:
               dict_rsi['re_cpu_Background'].append(re_cpu_Background[0]+'%')
               #print(dict_rsi['re_cpu_Background'])
           
           re_cpu_Kernel = re.findall('      Kernel\ *(\d+)',each)
           if re_cpu_Kernel:
               dict_rsi['re_cpu_Kernel'].append(re_cpu_Kernel[0]+'%')
               #print(dict_rsi['re_cpu_Kernel'])
           
           re_cpu_Interrupt = re.findall('^      Interrupt\ *(\d+)',each)
           if re_cpu_Interrupt:
               dict_rsi['re_cpu_Interrupt'].append(re_cpu_Interrupt[0]+'%')
               #print(dict_rsi['re_cpu_Interrupt'])
           
           re_cpu_Idle = re.findall('Idle\ *(\d+)',each)
           if re_cpu_Idle:
               dict_rsi['re_cpu_Idle'].append(re_cpu_Idle[0]+'%')
               #print(dict_rsi['re_cpu_Idle'])
           
           re_refpc_starttime = re.findall('Start time\ *(.*)',each)
           if re_refpc_starttime:
               dict_rsi['re_refpc_starttime'].append(re_refpc_starttime[0])
               #print(dict_rsi['re_refpc_starttime'])
           
           re_refpc_uptime = re.findall('^\ *Uptime\ *(.*)',each)
           if re_refpc_uptime:
               dict_rsi['re_refpc_uptime'].append(re_refpc_uptime[0])
               while (':' in dict_rsi['re_refpc_uptime']):
                   dict_rsi['re_refpc_uptime'].remove(':')
               #print(dict_rsi['re_refpc_uptime'])
           
           re_last_reboot_reason = re.findall('Last reboot reason\ *(.*)',each)
           if re_last_reboot_reason:
               dict_rsi['re_last_reboot_reason'].append(re_last_reboot_reason[0])
               #print(dict_rsi['re_last_reboot_reason'])
           
           hw_Component = re.findall('.*Failed\ +[0-9]+ degrees C.*|.*Check\ +[0-9]+ degrees C.*|FPC [0-9]+ Power Supply.*Failed.*|FPC [0-9]+ Fan Tray.*Failed.*',each)
           if hw_Component:
               dict_rsi['hw_component'].append(hw_Component[0])
               while ('' in dict_rsi['hw_component']):
                   dict_rsi['hw_component'].remove('')
               #print(dict_rsi['hw_component'])
        j=0       
        for i in dict_rsi['hw_component']:
            dict_rsi['hw_component'][j] = i.strip()
            j+=1
          
        dict_rsi['fpc'] = list(set(dict_rsi['fpc']))
        #loop to sort FPC Details
        i=0
        for element in dict_rsi['fpc']:
            dict_rsi['fpc'][i] = int(int_conv(element))
            i+=1

        dict_rsi['fpc'].sort()
        #print(dict_rsi['fpc'])
        #print(pfe_trun_key)
        #print(dict_rsi['pfe_trun_key'])
        #print("PRINTING ENTIRE DICT")
        #print(dict_rsi)
        #print(dict_rsi['core'])
        #table
        mytable = PrettyTable(["Component","Value"])
        mytable.hrules=ALL
        #Add rows
        try:
            mytable.add_row(['Hostname',dict_rsi['hostname']])
        except KeyError:
            print("Hostname not found on RSI file "+RSI)

        try:    
            mytable.add_row(['Platform',dict_rsi['model']])
        except KeyError:
            print("Platform Details not found on RSI file "+RSI)

        try:
            mytable.add_row(['Junos_Version',dict_rsi['version']])
        except KeyError:
            print("JUNOS Version Details not found on RSI file "+RSI+R+"\nPlease check if RSI file "+RSI+" contains valid info"+N)
            print(R+"EXITING THE HEALTHCHECK"+N)
            exit(1)

        if dict_rsi.get('host_version') != None:
            mytable.add_row(['Host-Version',dict_rsi['host_version']])
        mytable.add_row(['Uptime',dict_rsi['uptime']])
        if len(dict_rsi['alarm']) >= 1:
            i = 1
            for al in dict_rsi['alarm']:
                mytable.add_row(['Alarm'+' '+str(i),R+al+N])
                i = i+1
        else:
            mytable.add_row(['Alarm','No Alarms Present'])
       
        if dict_rsi.get('core') != None:
            if dict_rsi['core'] != []:
                i = 1
                for cor in dict_rsi['core']:
                   mytable.add_row(['Core'+' '+str(i),R+cor+N])
                   i+=1
            else:       
                mytable.add_row(['Core','No Cores Present'])


        if dict_rsi['process_nonzero']:
           for proc in dict_rsi['process_nonzero']:
               var = re.findall('([0-9]+\.[0-9]+).*\{(.*)\}|([0-9]+\.[0-9]+)%\ ([a-z]+)',proc)
               var = list(var[0])
               while ('' in var):
                   var.remove('')
               if 'idle' in var[1]:
                   if float(var[0]) < 50:
                       mytable.add_row([var[1],R+var[0]+'%'+N])
                   else:    
                       mytable.add_row([var[1],var[0]+'%'])
               else:    
                   if float(var[0]) > 50:
                       mytable.add_row([var[1]+' process CPU usage',R+var[0]+'%'+N])
                   else:
                       mytable.add_row([var[1]+' process CPU usage',var[0]+'%'])
        
        #process memory display
        try:
            if len(dict_rsi['mem']) == 5:
                mytable.add_row(['Active Memory',dict_rsi['mem'][0]])
                mytable.add_row(['InActive Memory',dict_rsi['mem'][1]])
                mytable.add_row(['Wired Memory',dict_rsi['mem'][2]])
                mytable.add_row(['Buffer Memory',dict_rsi['mem'][3]])
                mytable.add_row(['Free Memory',dict_rsi['mem'][4]])
                #usable_mem = int(dict_rsi['mem'][1])+int(dict_rsi['mem'][3])+int(dict_rsi['mem'][4])
                #mytable.add_row(['Overall Usable Memory',str(usable_mem)+'M'])
            else: 
                mytable.add_row(['Active Memory',dict_rsi['mem'][0]])
                mytable.add_row(['InActive Memory',dict_rsi['mem'][1]])
                mytable.add_row(['Wired Memory',dict_rsi['mem'][2]])
                mytable.add_row(['Cache Memory',dict_rsi['mem'][3]])
                mytable.add_row(['Buffer Memory',dict_rsi['mem'][4]])
                mytable.add_row(['Free Memory',dict_rsi['mem'][5]])
        except KeyError:
        #Laundry memory display
            try:
                mytable.add_row(['Active Memory',dict_rsi['laun'][0]])
                mytable.add_row(['InActive Memory',dict_rsi['laun'][1]])
                mytable.add_row(['Laundry Memory',dict_rsi['laun'][2]])
                mytable.add_row(['Wired Memory',dict_rsi['laun'][3]])
                mytable.add_row(['Buffer Memory',dict_rsi['laun'][4]])
                mytable.add_row(['Free Memory',dict_rsi['laun'][5]])
            
            except KeyError:
                print("Check Process Memory pattern in the code")
            
        #swap mem display
        if dict_rsi.get('swap') != None:
            if len(dict_rsi['swap']) > 2:
                 mytable.add_row(['Swap Total',dict_rsi['swap'][0]])
                 mytable.add_row(['Swap Used',dict_rsi['swap'][1]])
                 mytable.add_row(['Swap Free',dict_rsi['swap'][2]])
                 swap_in_use = re.findall('[0-9]+',dict_rsi['swap'][3])
                 if int(swap_in_use[0]) > 50:
                     mytable.add_row(['Swap Inuse Percentage',R+dict_rsi['swap'][3]+N])
                 else:
                     mytable.add_row(['Swap Inuse Percentage',dict_rsi['swap'][3]])
            else:
                 mytable.add_row(['Swap Total',dict_rsi['swap'][0]])
                 mytable.add_row(['Swap Free',dict_rsi['swap'][1]])
                 mytable.add_row(['Swap Free Percentage','100%'])
      

        #Print RE Type
        if dict_rsi['re'] != []:
            mytable.add_row(['RE Type',dict_rsi['re'][0][0]])

        if len(dict_rsi['re_role']) > 1:
            #print(len(dict_rsi['re_role']))
            #print(dict_rsi['re_role'])
            mytable.add_row(['RE0 role',dict_rsi['re_role'][0]])
            if int_conv(dict_rsi['re_mem'][0]) > 80:
                mytable.add_row(['RE0 Memory usage',R+dict_rsi['re_mem'][0]+N])
            else:
                mytable.add_row(['RE0 Memory usage',dict_rsi['re_mem'][0]])
            mytable.add_row(['RE0 Start time',dict_rsi['re_refpc_starttime'][0]])
            mytable.add_row(['RE0 Uptime',dict_rsi['re_refpc_uptime'][0]])
            mytable.add_row(['RE0 Last reboot reason',dict_rsi['re_last_reboot_reason'][0]])
            mytable.add_row(['RE1 role',dict_rsi['re_role'][1]])
            if int_conv(dict_rsi['re_mem'][1]) > 80:
                mytable.add_row(['RE1 Memory usage',R+dict_rsi['re_mem'][1]+N])
            else:
                mytable.add_row(['RE1 Memory usage',dict_rsi['re_mem'][1]])
            mytable.add_row(['RE1 Start time',dict_rsi['re_refpc_starttime'][1]])
            mytable.add_row(['RE1 Uptime',dict_rsi['re_refpc_uptime'][1]])
            mytable.add_row(['RE1 Last reboot reason',dict_rsi['re_last_reboot_reason'][1]])
            
            if dict_rsi['re_role'][0] == 'Master' and len(dict_rsi['re_cpu_user']) == 5:
                 
                 #User process CPU usage
                 if int_conv(dict_rsi['re_cpu_user'][0]) > 9 and int_conv(dict_rsi['re_cpu_user'][0]) < 50:
                     mytable.add_row(['Master RE0 5 Sec User CPU usage',dict_rsi['re_cpu_user'][0]])
                 elif int_conv(dict_rsi['re_cpu_user'][0]) > 49:
                     mytable.add_row(['Master RE0 5 Sec User CPU usage',R+dict_rsi['re_cpu_user'][0]+N])
                 
                 if int_conv(dict_rsi['re_cpu_user'][1]) > 9 and int_conv(dict_rsi['re_cpu_user'][1]) < 50:
                     mytable.add_row(['Master RE0 1 Min User CPU usage',dict_rsi['re_cpu_user'][1]])
                 elif int_conv(dict_rsi['re_cpu_user'][1]) > 49:
                     mytable.add_row(['Master RE0 1 Min User CPU usage',R+dict_rsi['re_cpu_user'][1]+N])

                 if int_conv(dict_rsi['re_cpu_user'][2]) > 9 and int_conv(dict_rsi['re_cpu_user'][2]) < 50:
                     mytable.add_row(['Master RE0 5 Min User CPU usage',dict_rsi['re_cpu_user'][2]])
                 elif int_conv(dict_rsi['re_cpu_user'][2]) > 49:
                     mytable.add_row(['Master RE0 5 Min User CPU usage',R+dict_rsi['re_cpu_user'][2]+N])
                 
                 if int_conv(dict_rsi['re_cpu_user'][3]) > 9 and int_conv(dict_rsi['re_cpu_user'][3]) < 50:
                     mytable.add_row(['Master RE0 15 Min User CPU usage',dict_rsi['re_cpu_user'][3]])
                 elif int_conv(dict_rsi['re_cpu_user'][3]) > 49:
                     mytable.add_row(['Master RE0 15 Min User CPU usage',R+dict_rsi['re_cpu_user'][3]+N])
                 
                 if int_conv(dict_rsi['re_cpu_user'][4]) > 9 and int_conv(dict_rsi['re_cpu_user'][4]) < 50:
                     mytable.add_row(['Backup RE1 15 Min User CPU usage',dict_rsi['re_cpu_user'][4]])
                 elif int_conv(dict_rsi['re_cpu_user'][4]) > 49:
                     mytable.add_row(['Backup RE1 15 Min User CPU usage',R+dict_rsi['re_cpu_user'][4]+N])
                 
                 
                 #Background process CPU usage
                 if int_conv(dict_rsi['re_cpu_Background'][0]) > 9 and int_conv(dict_rsi['re_cpu_Background'][0]) < 50:
                     mytable.add_row(['Master RE0 5 Sec Background CPU usage',dict_rsi['re_cpu_Background'][0]])
                 elif int_conv(dict_rsi['re_cpu_Background'][0]) > 49:
                     mytable.add_row(['Master RE0 5 Sec Background CPU usage',R+dict_rsi['re_cpu_Background'][0]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Background'][1]) > 9 and int_conv(dict_rsi['re_cpu_Background'][1]) < 50:
                     mytable.add_row(['Master RE0 1 Min Background CPU usage',dict_rsi['re_cpu_Background'][1]])
                 elif int_conv(dict_rsi['re_cpu_Background'][1]) > 49:
                     mytable.add_row(['Master RE0 1 Min Background CPU usage',R+dict_rsi['re_cpu_Background'][1]+N])
                
                 if int_conv(dict_rsi['re_cpu_Background'][2]) > 9 and int_conv(dict_rsi['re_cpu_Background'][2]) < 50:
                     mytable.add_row(['Master RE0 5 Min Background CPU usage',dict_rsi['re_cpu_Background'][2]])
                 elif int_conv(dict_rsi['re_cpu_Background'][2]) > 49:
                     mytable.add_row(['Master RE0 5 Min Background CPU usage',R+dict_rsi['re_cpu_Background'][2]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Background'][3]) > 9 and int_conv(dict_rsi['re_cpu_Background'][3]) < 50:
                     mytable.add_row(['Master RE0 15 Min Background CPU usage',dict_rsi['re_cpu_Background'][3]])
                 elif int_conv(dict_rsi['re_cpu_Background'][3]) > 49:
                     mytable.add_row(['Master RE0 15 Min Background CPU usage',R+dict_rsi['re_cpu_Background'][3]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Background'][4]) > 9 and int_conv(dict_rsi['re_cpu_Background'][4]) < 50:
                     mytable.add_row(['Backup RE1 15 Min Background CPU usage',dict_rsi['re_cpu_Background'][4]])
                 elif int_conv(dict_rsi['re_cpu_Background'][4]) > 49:
                     mytable.add_row(['Backup RE1 15 Min Background CPU usage',R+dict_rsi['re_cpu_Background'][4]+N])
                

                 #Kernel process CPU usage
                 if int_conv(dict_rsi['re_cpu_Kernel'][0]) > 9 and int_conv(dict_rsi['re_cpu_Kernel'][0]) < 50:
                     mytable.add_row(['Master RE0 5 Sec Kernel CPU usage',dict_rsi['re_cpu_Kernel'][0]])
                 elif int_conv(dict_rsi['re_cpu_Kernel'][0]) > 49:
                     mytable.add_row(['Master RE0 5 Sec Kernel CPU usage',R+dict_rsi['re_cpu_Kernel'][0]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Kernel'][1]) > 9 and int_conv(dict_rsi['re_cpu_Kernel'][1]) < 50:
                     mytable.add_row(['Master RE0 1 Min Kernel CPU usage',dict_rsi['re_cpu_Kernel'][1]])
                 elif int_conv(dict_rsi['re_cpu_Kernel'][1]) > 49:
                     mytable.add_row(['Master RE0 1 Min Kernel CPU usage',R+dict_rsi['re_cpu_Kernel'][1]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Kernel'][2]) > 9 and int_conv(dict_rsi['re_cpu_Kernel'][2]) < 50:
                     mytable.add_row(['Master RE0 5 Min Kernel CPU usage',dict_rsi['re_cpu_Kernel'][2]])
                 elif int_conv(dict_rsi['re_cpu_Kernel'][2]) > 49:
                     mytable.add_row(['Master RE0 5 Min Kernel CPU usage',R+dict_rsi['re_cpu_Kernel'][2]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Kernel'][3]) > 9 and int_conv(dict_rsi['re_cpu_Kernel'][3]) < 50:
                     mytable.add_row(['Master RE0 15 Min Kernel CPU usage',dict_rsi['re_cpu_Kernel'][3]])
                 elif int_conv(dict_rsi['re_cpu_Kernel'][3]) > 49:
                     mytable.add_row(['Master RE0 15 Min Kernel CPU usage',R+dict_rsi['re_cpu_Kernel'][3]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Kernel'][4]) > 9 and int_conv(dict_rsi['re_cpu_Kernel'][4]) < 50:
                     mytable.add_row(['Backup RE1 15 Min Kernel CPU usage',dict_rsi['re_cpu_Kernel'][4]])
                 elif int_conv(dict_rsi['re_cpu_Kernel'][4]) > 49:
                     mytable.add_row(['Backup RE1 15 Min Kernel CPU usage',R+dict_rsi['re_cpu_Kernel'][4]+N])
                 
       
                 #Interrupt process CPU usage
                 if int_conv(dict_rsi['re_cpu_Interrupt'][0]) > 9 and int_conv(dict_rsi['re_cpu_Interrupt'][0]) < 50:
                     mytable.add_row(['Master RE0 5 Sec Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][0]])
                 elif int_conv(dict_rsi['re_cpu_Interrupt'][0]) > 49:
                     mytable.add_row(['Master RE0 5 Sec Interrupt CPU usage',R+dict_rsi['re_cpu_Interrupt'][0]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Interrupt'][1]) > 9 and int_conv(dict_rsi['re_cpu_Interrupt'][1]) < 50:
                     mytable.add_row(['Master RE0 1 Min Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][1]])
                 elif int_conv(dict_rsi['re_cpu_Interrupt'][1]) > 49:
                     mytable.add_row(['Master RE0 1 Min Interrupt CPU usage',R+dict_rsi['re_cpu_Interrupt'][1]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Interrupt'][2]) > 9 and int_conv(dict_rsi['re_cpu_Interrupt'][2]) < 50:
                     mytable.add_row(['Master RE0 5 Min Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][2]])
                 elif int_conv(dict_rsi['re_cpu_Interrupt'][2]) > 49:
                     mytable.add_row(['Master RE0 5 Min Interrupt CPU usage',R+dict_rsi['re_cpu_Interrupt'][2]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Interrupt'][3]) > 9 and int_conv(dict_rsi['re_cpu_Interrupt'][3]) < 50:
                     mytable.add_row(['Master RE0 15 Min Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][3]])
                 elif int_conv(dict_rsi['re_cpu_Interrupt'][3]) > 49:
                     mytable.add_row(['Master RE0 15 Min Interrupt CPU usage',R+dict_rsi['re_cpu_Interrupt'][3]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Interrupt'][4]) > 9 and int_conv(dict_rsi['re_cpu_Interrupt'][4]) < 50:
                     mytable.add_row(['Backup RE1 15 Min Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][4]])
                 elif int_conv(dict_rsi['re_cpu_Interrupt'][4]) > 49:
                     mytable.add_row(['Backup RE1 15 Min Interrupt CPU usage',R+dict_rsi['re_cpu_Interrupt'][4]+N])
                

                 #IDLE CPU 
                 if int_conv(dict_rsi['re_cpu_Idle'][0]) < 30:
                     mytable.add_row(['Master RE0 5 Sec Idle CPU',R+dict_rsi['re_cpu_Idle'][0]+N])
                 else:
                     mytable.add_row(['Master RE0 5 Sec Idle CPU',dict_rsi['re_cpu_Idle'][0]])
                
                 if int_conv(dict_rsi['re_cpu_Idle'][1]) < 30:
                     mytable.add_row(['Master RE0 1 Min Idle CPU',R+dict_rsi['re_cpu_Idle'][1]+N])
                 else:
                     mytable.add_row(['Master RE0 1 Min Idle CPU',dict_rsi['re_cpu_Idle'][1]])
                 
                 if int_conv(dict_rsi['re_cpu_Idle'][2]) < 30:
                     mytable.add_row(['Master RE0 5 Min Idle CPU',R+dict_rsi['re_cpu_Idle'][2]+N])
                 else:
                     mytable.add_row(['Master RE0 5 Min Idle CPU',dict_rsi['re_cpu_Idle'][2]])
                 
                 if int_conv(dict_rsi['re_cpu_Idle'][3]) < 30:
                     mytable.add_row(['Master RE0 15 Min Idle CPU',R+dict_rsi['re_cpu_Idle'][3]+N])
                 else:
                     mytable.add_row(['Master RE0 15 Min Idle CPU',dict_rsi['re_cpu_Idle'][3]])
                 
                 if int_conv(dict_rsi['re_cpu_Idle'][4]) < 30:
                     mytable.add_row(['Backup RE1 15 Min Idle CPU',R+dict_rsi['re_cpu_Idle'][4]+N])
                 else:
                     mytable.add_row(['Backup RE1 15 Min Idle CPU',dict_rsi['re_cpu_Idle'][4]])
                 
            elif dict_rsi['re_role'][0] == 'Backup' and len(dict_rsi['re_cpu_user']) == 5:
                 
                 #User process CPU usage
                 if int_conv(dict_rsi['re_cpu_user'][1]) > 9 and int_conv(dict_rsi['re_cpu_user'][1]) < 50:
                     mytable.add_row(['Master RE1 5 Sec User CPU usage',dict_rsi['re_cpu_user'][1]])
                 elif int_conv(dict_rsi['re_cpu_user'][1]) > 49:
                     mytable.add_row(['Master RE1 5 Sec User CPU usage',R+dict_rsi['re_cpu_user'][1]+N])
                 
                 if int_conv(dict_rsi['re_cpu_user'][2]) > 9 and int_conv(dict_rsi['re_cpu_user'][2]) < 50:
                     mytable.add_row(['Master RE1 1 Min User CPU usage',dict_rsi['re_cpu_user'][2]])
                 elif int_conv(dict_rsi['re_cpu_user'][2]) > 49:
                     mytable.add_row(['Master RE1 1 Min User CPU usage',R+dict_rsi['re_cpu_user'][2]+N])

                 if int_conv(dict_rsi['re_cpu_user'][3]) > 9 and int_conv(dict_rsi['re_cpu_user'][3]) < 50:
                     mytable.add_row(['Master RE1 5 Min User CPU usage',dict_rsi['re_cpu_user'][3]])
                 elif int_conv(dict_rsi['re_cpu_user'][3]) > 49:
                     mytable.add_row(['Master RE1 5 Min User CPU usage',R+dict_rsi['re_cpu_user'][3]+N])
                 
                 if int_conv(dict_rsi['re_cpu_user'][4]) > 9 and int_conv(dict_rsi['re_cpu_user'][4]) < 50:
                     mytable.add_row(['Master RE1 15 Min User CPU usage',dict_rsi['re_cpu_user'][4]])
                 elif int_conv(dict_rsi['re_cpu_user'][4]) > 49:
                     mytable.add_row(['Master RE1 15 Min User CPU usage',R+dict_rsi['re_cpu_user'][4]+N])
                 
                 if int_conv(dict_rsi['re_cpu_user'][0]) > 9 and int_conv(dict_rsi['re_cpu_user'][0]) < 50:
                     mytable.add_row(['Backup RE0 15 Min User CPU usage',dict_rsi['re_cpu_user'][0]])
                 elif int_conv(dict_rsi['re_cpu_user'][0]) > 49:
                     mytable.add_row(['Backup RE0 15 Min User CPU usage',R+dict_rsi['re_cpu_user'][0]+N])
                 
                 
                 #Background process CPU usage
                 if int_conv(dict_rsi['re_cpu_Background'][1]) > 9 and int_conv(dict_rsi['re_cpu_Background'][1]) < 50:
                     mytable.add_row(['Master RE1 5 Sec Background CPU usage',dict_rsi['re_cpu_Background'][1]])
                 elif int_conv(dict_rsi['re_cpu_Background'][1]) > 49:
                     mytable.add_row(['Master RE1 5 Sec Background CPU usage',R+dict_rsi['re_cpu_Background'][1]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Background'][2]) > 9 and int_conv(dict_rsi['re_cpu_Background'][2]) < 50:
                     mytable.add_row(['Master RE1 1 Min Background CPU usage',dict_rsi['re_cpu_Background'][2]])
                 elif int_conv(dict_rsi['re_cpu_Background'][2]) > 49:
                     mytable.add_row(['Master RE1 1 Min Background CPU usage',R+dict_rsi['re_cpu_Background'][2]+N])
                
                 if int_conv(dict_rsi['re_cpu_Background'][3]) > 9 and int_conv(dict_rsi['re_cpu_Background'][3]) < 50:
                     mytable.add_row(['Master RE1 5 Min Background CPU usage',dict_rsi['re_cpu_Background'][3]])
                 elif int_conv(dict_rsi['re_cpu_Background'][3]) > 49:
                     mytable.add_row(['Master RE1 5 Min Background CPU usage',R+dict_rsi['re_cpu_Background'][3]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Background'][4]) > 9 and int_conv(dict_rsi['re_cpu_Background'][4]) < 50:
                     mytable.add_row(['Master RE1 15 Min Background CPU usage',dict_rsi['re_cpu_Background'][4]])
                 elif int_conv(dict_rsi['re_cpu_Background'][4]) > 49:
                     mytable.add_row(['Master RE1 15 Min Background CPU usage',R+dict_rsi['re_cpu_Background'][4]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Background'][0]) > 9 and int_conv(dict_rsi['re_cpu_Background'][0]) < 50:
                     mytable.add_row(['Backup RE0 15 Min Background CPU usage',dict_rsi['re_cpu_Background'][0]])
                 elif int_conv(dict_rsi['re_cpu_Background'][0]) > 49:
                     mytable.add_row(['Backup RE0 15 Min Background CPU usage',R+dict_rsi['re_cpu_Background'][0]+N])
                

                 #Kernel process CPU usage
                 if int_conv(dict_rsi['re_cpu_Kernel'][1]) > 9 and int_conv(dict_rsi['re_cpu_Kernel'][1]) < 50:
                     mytable.add_row(['Master RE1 5 Sec Kernel CPU usage',dict_rsi['re_cpu_Kernel'][1]])
                 elif int_conv(dict_rsi['re_cpu_Kernel'][1]) > 49:
                     mytable.add_row(['Master RE1 5 Sec Kernel CPU usage',R+dict_rsi['re_cpu_Kernel'][1]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Kernel'][2]) > 9 and int_conv(dict_rsi['re_cpu_Kernel'][2]) < 50:
                     mytable.add_row(['Master RE1 1 Min Kernel CPU usage',dict_rsi['re_cpu_Kernel'][2]])
                 elif int_conv(dict_rsi['re_cpu_Kernel'][2]) > 49:
                     mytable.add_row(['Master RE1 1 Min Kernel CPU usage',R+dict_rsi['re_cpu_Kernel'][2]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Kernel'][3]) > 9 and int_conv(dict_rsi['re_cpu_Kernel'][3]) < 50:
                     mytable.add_row(['Master RE1 5 Min Kernel CPU usage',dict_rsi['re_cpu_Kernel'][3]])
                 elif int_conv(dict_rsi['re_cpu_Kernel'][3]) > 49:
                     mytable.add_row(['Master RE1 5 Min Kernel CPU usage',R+dict_rsi['re_cpu_Kernel'][3]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Kernel'][4]) > 9 and int_conv(dict_rsi['re_cpu_Kernel'][4]) < 50:
                     mytable.add_row(['Master RE1 15 Min Kernel CPU usage',dict_rsi['re_cpu_Kernel'][4]])
                 elif int_conv(dict_rsi['re_cpu_Kernel'][4]) > 49:
                     mytable.add_row(['Master RE1 15 Min Kernel CPU usage',R+dict_rsi['re_cpu_Kernel'][4]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Kernel'][0]) > 9 and int_conv(dict_rsi['re_cpu_Kernel'][0]) < 50:
                     mytable.add_row(['Backup RE0 15 Min Kernel CPU usage',dict_rsi['re_cpu_Kernel'][0]])
                 elif int_conv(dict_rsi['re_cpu_Kernel'][0]) > 49:
                     mytable.add_row(['Backup RE0 15 Min Kernel CPU usage',R+dict_rsi['re_cpu_Kernel'][0]+N])
                 
       
                 #Interrupt process CPU usage
                 if int_conv(dict_rsi['re_cpu_Interrupt'][1]) > 9 and int_conv(dict_rsi['re_cpu_Interrupt'][1]) < 50:
                     mytable.add_row(['Master RE1 5 Sec Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][1]])
                 elif int_conv(dict_rsi['re_cpu_Interrupt'][1]) > 49:
                     mytable.add_row(['Master RE1 5 Sec Interrupt CPU usage',R+dict_rsi['re_cpu_Interrupt'][1]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Interrupt'][2]) > 9 and int_conv(dict_rsi['re_cpu_Interrupt'][2]) < 50:
                     mytable.add_row(['Master RE1 1 Min Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][2]])
                 elif int_conv(dict_rsi['re_cpu_Interrupt'][2]) > 49:
                     mytable.add_row(['Master RE1 1 Min Interrupt CPU usage',R+dict_rsi['re_cpu_Interrupt'][2]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Interrupt'][3]) > 9 and int_conv(dict_rsi['re_cpu_Interrupt'][3]) < 50:
                     mytable.add_row(['Master RE1 5 Min Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][3]])
                 elif int_conv(dict_rsi['re_cpu_Interrupt'][3]) > 49:
                     mytable.add_row(['Master RE1 5 Min Interrupt CPU usage',R+dict_rsi['re_cpu_Interrupt'][3]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Interrupt'][4]) > 9 and int_conv(dict_rsi['re_cpu_Interrupt'][4]) < 50:
                     mytable.add_row(['Master RE1 15 Min Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][4]])
                 elif int_conv(dict_rsi['re_cpu_Interrupt'][4]) > 49:
                     mytable.add_row(['Master RE1 15 Min Interrupt CPU usage',R+dict_rsi['re_cpu_Interrupt'][4]+N])
                 
                 if int_conv(dict_rsi['re_cpu_Interrupt'][0]) > 9 and int_conv(dict_rsi['re_cpu_Interrupt'][0]) < 50:
                     mytable.add_row(['Backup RE0 15 Min Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][0]])
                 elif int_conv(dict_rsi['re_cpu_Interrupt'][0]) > 49:
                     mytable.add_row(['Backup RE0 15 Min Interrupt CPU usage',R+dict_rsi['re_cpu_Interrupt'][0]+N])
                

                 #IDLE CPU 
                 if int_conv(dict_rsi['re_cpu_Idle'][1]) < 30:
                     mytable.add_row(['Master RE1 5 Sec Idle CPU',R+dict_rsi['re_cpu_Idle'][1]+N])
                 else:
                     mytable.add_row(['Master RE1 5 Sec Idle CPU',dict_rsi['re_cpu_Idle'][1]])
                
                 if int_conv(dict_rsi['re_cpu_Idle'][2]) < 30:
                     mytable.add_row(['Master RE1 1 Min Idle CPU',R+dict_rsi['re_cpu_Idle'][2]+N])
                 else:
                     mytable.add_row(['Master RE1 1 Min Idle CPU',dict_rsi['re_cpu_Idle'][2]])
                 
                 if int_conv(dict_rsi['re_cpu_Idle'][3]) < 30:
                     mytable.add_row(['Master RE1 5 Min Idle CPU',R+dict_rsi['re_cpu_Idle'][3]+N])
                 else:
                     mytable.add_row(['Master RE1 5 Min Idle CPU',dict_rsi['re_cpu_Idle'][3]])
                 
                 if int_conv(dict_rsi['re_cpu_Idle'][4]) < 30:
                     mytable.add_row(['Master RE1 15 Min Idle CPU',R+dict_rsi['re_cpu_Idle'][4]+N])
                 else:
                     mytable.add_row(['Master RE1 15 Min Idle CPU',dict_rsi['re_cpu_Idle'][4]])
                 
                 if int_conv(dict_rsi['re_cpu_Idle'][0]) < 30:
                     mytable.add_row(['Backup RE0 15 Min Idle CPU',R+dict_rsi['re_cpu_Idle'][0]+N])
                 else:
                     mytable.add_row(['Backup RE0 15 Min Idle CPU',dict_rsi['re_cpu_Idle'][0]])
                 
                 #mytable.add_row(['Master RE1 5 Sec User CPU usage',dict_rsi['re_cpu_user'][1]])
                 #mytable.add_row(['Master RE1 1 Min User CPU usage',dict_rsi['re_cpu_user'][2]])
                 #mytable.add_row(['Master RE1 5 Min User CPU usage',dict_rsi['re_cpu_user'][3]])
                 #mytable.add_row(['Master RE1 15 Min User CPU usage',dict_rsi['re_cpu_user'][4]])
                 #mytable.add_row(['Backup RE0 15 Min User CPU usage',dict_rsi['re_cpu_user'][0]])

                 #mytable.add_row(['Master RE1 5 Sec Background CPU usage',dict_rsi['re_cpu_Background'][1]])
                 #mytable.add_row(['Master RE1 1 Min Background CPU usage',dict_rsi['re_cpu_Background'][2]])
                 #mytable.add_row(['Master RE1 5 Min Background CPU usage',dict_rsi['re_cpu_Background'][3]])
                 #mytable.add_row(['Master RE1 15 Min Background CPU usage',dict_rsi['re_cpu_Background'][4]])
                 #mytable.add_row(['Backup RE0 15 Min Background CPU usage',dict_rsi['re_cpu_Background'][0]])

                 #mytable.add_row(['Master RE1 5 Sec Kernel CPU usage',dict_rsi['re_cpu_Kernel'][1]])
                 #mytable.add_row(['Master RE1 1 Min Kernel CPU usage',dict_rsi['re_cpu_Kernel'][2]])
                 #mytable.add_row(['Master RE1 5 Min Kernel CPU usage',dict_rsi['re_cpu_Kernel'][3]])
                 #mytable.add_row(['Master RE1 15 Min Kernel CPU usage',dict_rsi['re_cpu_Kernel'][4]])
                 #mytable.add_row(['Backup RE0 15 Min Kernel CPU usage',dict_rsi['re_cpu_Kernel'][0]])

                 #mytable.add_row(['Master RE1 5 Sec Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][1]])
                 #mytable.add_row(['Master RE1 1 Min Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][2]])
                 #mytable.add_row(['Master RE1 5 Min Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][3]])
                 #mytable.add_row(['Master RE1 15 Min Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][4]])
                 #mytable.add_row(['Backup RE0 15 Min Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][0]])

                 #mytable.add_row(['Master RE1 5 Sec Idle CPU',dict_rsi['re_cpu_Idle'][1]])
                 #mytable.add_row(['Master RE1 1 Min Idle CPU',dict_rsi['re_cpu_Idle'][2]])
                 #mytable.add_row(['Master RE1 5 Min Idle CPU',dict_rsi['re_cpu_Idle'][3]])
                 #mytable.add_row(['Master RE1 15 Min Idle CPU',dict_rsi['re_cpu_Idle'][4]])
                 #mytable.add_row(['Backup RE0 15 Min Idle CPU',dict_rsi['re_cpu_Idle'][0]])
           
            else:
                 if int_conv(dict_rsi['re_cpu_user'][0]) > 9 and int_conv(dict_rsi['re_cpu_user'][0]) < 50:
                     mytable.add_row(['RE0 5 Sec User CPU usage',dict_rsi['re_cpu_user'][0]])
                 elif int_conv(dict_rsi['re_cpu_user'][0]) > 49:
                     mytable.add_row(['RE0 5 Sec User CPU usage',R+dict_rsi['re_cpu_user'][0]+N])
                 
                 if int_conv(dict_rsi['re_cpu_user'][1]) > 9 and int_conv(dict_rsi['re_cpu_user'][1]) < 50:
                     mytable.add_row(['RE1 5 Sec User CPU usage',dict_rsi['re_cpu_user'][1]])
                 elif int_conv(dict_rsi['re_cpu_user'][1]) > 49:
                     mytable.add_row(['RE1 5 Sec User CPU usage',R+dict_rsi['re_cpu_user'][1]+N])


        else:
            mytable.add_row(['RE Role',dict_rsi['re_role'][0]])
            if int_conv(dict_rsi['re_mem'][0]) > 80:
                mytable.add_row(['RE0 Memory usage',R+dict_rsi['re_mem'][0]+N])
            else:
                mytable.add_row(['RE0 Memory usage',dict_rsi['re_mem'][0]])
            mytable.add_row(['RE0 Start time',dict_rsi['re_refpc_starttime'][0]])
            mytable.add_row(['RE0 Uptime',dict_rsi['re_refpc_uptime'][0]])

            mytable.add_row(['RE0 Last reboot reason',dict_rsi['re_last_reboot_reason'][0]])
          

            if len(dict_rsi['re_cpu_user']) == 1: #for facebook ex4300-48t SR:2024-0403-119016 RSI

            #User process CPU
                if int_conv(dict_rsi['re_cpu_user'][0]) > 9 and int_conv(dict_rsi['re_cpu_user'][0]) < 50:
                    mytable.add_row(['Master RE0 5 Sec User CPU usage',dict_rsi['re_cpu_user'][0]])
                elif int_conv(dict_rsi['re_cpu_user'][0]) > 49:
                    mytable.add_row(['Master RE0 5 Sec User CPU usage',R+dict_rsi['re_cpu_user'][0]+N])

            #Background process CPU
                if int_conv(dict_rsi['re_cpu_Background'][0]) > 9 and int_conv(dict_rsi['re_cpu_Background'][0]) < 50:
                    mytable.add_row(['Master RE0 5 Sec Background CPU usage',dict_rsi['re_cpu_Background'][0]])
                elif int_conv(dict_rsi['re_cpu_Background'][0]) > 49:
                    mytable.add_row(['Master RE0 5 Sec Background CPU usage',R+dict_rsi['re_cpu_Background'][0]+N])

            #Kernel process CPU
                if int_conv(dict_rsi['re_cpu_Kernel'][0]) > 9 and int_conv(dict_rsi['re_cpu_Kernel'][0]) < 50:
                    mytable.add_row(['Master RE0 5 Sec Kernel CPU usage',dict_rsi['re_cpu_Kernel'][0]])
                elif int_conv(dict_rsi['re_cpu_Kernel'][0]) > 49:
                    mytable.add_row(['Master RE0 5 Sec Kernel CPU usage',R+dict_rsi['re_cpu_Kernel'][0]+N])

            #Kernel process CPU
                if int_conv(dict_rsi['re_cpu_Kernel'][0]) > 9 and int_conv(dict_rsi['re_cpu_Kernel'][0]) < 50:
                    mytable.add_row(['Master RE0 5 Sec Kernel CPU usage',dict_rsi['re_cpu_Kernel'][0]])
                elif int_conv(dict_rsi['re_cpu_Kernel'][0]) > 49:
                    mytable.add_row(['Master RE0 5 Sec Kernel CPU usage',R+dict_rsi['re_cpu_Kernel'][0]+N])

            #Interrupt process CPU   
                if int_conv(dict_rsi['re_cpu_Interrupt'][0]) > 9 and int_conv(dict_rsi['re_cpu_Interrupt'][0]) < 50:
                    mytable.add_row(['Master RE0 5 Sec Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][0]])
                elif int_conv(dict_rsi['re_cpu_Interrupt'][0]) > 49:
                    mytable.add_row(['Master RE0 5 Sec Interrupt CPU usage',R+dict_rsi['re_cpu_Interrupt'][0]+N])

            #IDLE CPU    
                if int_conv(dict_rsi['re_cpu_Idle'][0]) < 30:
                    mytable.add_row(['Master RE0 5 Sec Idle CPU',R+dict_rsi['re_cpu_Idle'][0]+N])
                else:
                    mytable.add_row(['Master RE0 5 Sec Idle CPU',dict_rsi['re_cpu_Idle'][0]])
            

            else:
            #for CPU usages having 5sec,1min,5min,15 min usage details         
            #User process CPU
                if int_conv(dict_rsi['re_cpu_user'][0]) > 9 and int_conv(dict_rsi['re_cpu_user'][0]) < 50:
                    mytable.add_row(['Master RE0 5 Sec User CPU usage',dict_rsi['re_cpu_user'][0]])
                elif int_conv(dict_rsi['re_cpu_user'][0]) > 49:
                    mytable.add_row(['Master RE0 5 Sec User CPU usage',R+dict_rsi['re_cpu_user'][0]+N])
 
                if int_conv(dict_rsi['re_cpu_user'][1]) > 9 and int_conv(dict_rsi['re_cpu_user'][1]) < 50:
                    mytable.add_row(['Master RE0 1 Min User CPU usage',dict_rsi['re_cpu_user'][1]])
                elif int_conv(dict_rsi['re_cpu_user'][1]) > 49:
                    mytable.add_row(['Master RE0 1 Min User CPU usage',R+dict_rsi['re_cpu_user'][1]+N])
            
                if int_conv(dict_rsi['re_cpu_user'][2]) > 9 and int_conv(dict_rsi['re_cpu_user'][2]) < 50:
                    mytable.add_row(['Master RE0 5 Min User CPU usage',dict_rsi['re_cpu_user'][2]])
                elif int_conv(dict_rsi['re_cpu_user'][2]) > 49:
                    mytable.add_row(['Master RE0 5 Min User CPU usage',R+dict_rsi['re_cpu_user'][2]+N])
            
                if int_conv(dict_rsi['re_cpu_user'][3]) > 9 and int_conv(dict_rsi['re_cpu_user'][3]) < 50:
                    mytable.add_row(['Master RE0 15 Min User CPU usage',dict_rsi['re_cpu_user'][3]])
                elif int_conv(dict_rsi['re_cpu_user'][3]) > 49:
                    mytable.add_row(['Master RE0 15 Min User CPU usage',R+dict_rsi['re_cpu_user'][3]+N])
            

            #Background process CPU
                if int_conv(dict_rsi['re_cpu_Background'][0]) > 9 and int_conv(dict_rsi['re_cpu_Background'][0]) < 50:
                    mytable.add_row(['Master RE0 5 Sec Background CPU usage',dict_rsi['re_cpu_Background'][0]])
                elif int_conv(dict_rsi['re_cpu_Background'][0]) > 49:
                    mytable.add_row(['Master RE0 5 Sec Background CPU usage',R+dict_rsi['re_cpu_Background'][0]+N])

                if int_conv(dict_rsi['re_cpu_Background'][1]) > 9 and int_conv(dict_rsi['re_cpu_Background'][1]) < 50:
                    mytable.add_row(['Master RE0 1 Min Background CPU usage',dict_rsi['re_cpu_Background'][1]])
                elif int_conv(dict_rsi['re_cpu_Background'][1]) > 49:
                    mytable.add_row(['Master RE0 1 Min Background CPU usage',R+dict_rsi['re_cpu_Background'][1]+N])
            
                if int_conv(dict_rsi['re_cpu_Background'][2]) > 9 and int_conv(dict_rsi['re_cpu_Background'][2]) < 50:
                    mytable.add_row(['Master RE0 5 Min Background CPU usage',dict_rsi['re_cpu_Background'][2]])
                elif int_conv(dict_rsi['re_cpu_Background'][2]) > 49:
                    mytable.add_row(['Master RE0 5 Min Background CPU usage',R+dict_rsi['re_cpu_Background'][2]+N])
            
                if int_conv(dict_rsi['re_cpu_Background'][3]) > 9 and int_conv(dict_rsi['re_cpu_Background'][3]) < 50:
                    mytable.add_row(['Master RE0 15 Min Background CPU usage',dict_rsi['re_cpu_Background'][3]])
                elif int_conv(dict_rsi['re_cpu_Background'][3]) > 49:
                    mytable.add_row(['Master RE0 15 Min Background CPU usage',R+dict_rsi['re_cpu_Background'][3]+N])
                 
           
            #Kernel process CPU
                if int_conv(dict_rsi['re_cpu_Kernel'][0]) > 9 and int_conv(dict_rsi['re_cpu_Kernel'][0]) < 50:
                    mytable.add_row(['Master RE0 5 Sec Kernel CPU usage',dict_rsi['re_cpu_Kernel'][0]])
                elif int_conv(dict_rsi['re_cpu_Kernel'][0]) > 49:
                    mytable.add_row(['Master RE0 5 Sec Kernel CPU usage',R+dict_rsi['re_cpu_Kernel'][0]+N])

                if int_conv(dict_rsi['re_cpu_Kernel'][1]) > 9 and int_conv(dict_rsi['re_cpu_Kernel'][1]) < 50:
                    mytable.add_row(['Master RE0 1 Min Kernel CPU usage',dict_rsi['re_cpu_Kernel'][1]])
                elif int_conv(dict_rsi['re_cpu_Kernel'][1]) > 49:
                    mytable.add_row(['Master RE0 1 Min Kernel CPU usage',R+dict_rsi['re_cpu_Kernel'][1]+N])

                if int_conv(dict_rsi['re_cpu_Kernel'][2]) > 9 and int_conv(dict_rsi['re_cpu_Kernel'][2]) < 50:
                    mytable.add_row(['Master RE0 5 Min Kernel CPU usage',dict_rsi['re_cpu_Kernel'][2]])
                elif int_conv(dict_rsi['re_cpu_Kernel'][2]) > 49:
                    mytable.add_row(['Master RE0 5 Min Kernel CPU usage',R+dict_rsi['re_cpu_Kernel'][2]+N])
            
                if int_conv(dict_rsi['re_cpu_Kernel'][3]) > 9 and int_conv(dict_rsi['re_cpu_Kernel'][3]) < 50:
                    mytable.add_row(['Master RE0 15 Min Kernel CPU usage',dict_rsi['re_cpu_Kernel'][3]])
                elif int_conv(dict_rsi['re_cpu_Kernel'][3]) > 49:
                    mytable.add_row(['Master RE0 15 Min Kernel CPU usage',R+dict_rsi['re_cpu_Kernel'][3]+N])
               

            #Interrupt process CPU   
                if int_conv(dict_rsi['re_cpu_Interrupt'][0]) > 9 and int_conv(dict_rsi['re_cpu_Interrupt'][0]) < 50:
                    mytable.add_row(['Master RE0 5 Sec Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][0]])
                elif int_conv(dict_rsi['re_cpu_Interrupt'][0]) > 49:
                    mytable.add_row(['Master RE0 5 Sec Interrupt CPU usage',R+dict_rsi['re_cpu_Interrupt'][0]+N])

                if int_conv(dict_rsi['re_cpu_Interrupt'][1]) > 9 and int_conv(dict_rsi['re_cpu_Interrupt'][1]) < 50:
                    mytable.add_row(['Master RE0 1 Min Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][1]])
                elif int_conv(dict_rsi['re_cpu_Interrupt'][1]) > 49:
                    mytable.add_row(['Master RE0 1 Min Interrupt CPU usage',R+dict_rsi['re_cpu_Interrupt'][1]+N])
            
                if int_conv(dict_rsi['re_cpu_Interrupt'][2]) > 9 and int_conv(dict_rsi['re_cpu_Interrupt'][2]) < 50:
                    mytable.add_row(['Master RE0 5 Min Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][2]])
                elif int_conv(dict_rsi['re_cpu_Interrupt'][2]) > 49:
                    mytable.add_row(['Master RE0 5 Min Interrupt CPU usage',R+dict_rsi['re_cpu_Interrupt'][2]+N])
            
                if int_conv(dict_rsi['re_cpu_Interrupt'][3]) > 9 and int_conv(dict_rsi['re_cpu_Interrupt'][3]) < 50:
                    mytable.add_row(['Master RE0 15 Min Interrupt CPU usage',dict_rsi['re_cpu_Interrupt'][3]])
                elif int_conv(dict_rsi['re_cpu_Interrupt'][3]) > 49:
                    mytable.add_row(['Master RE0 15 Min Interrupt CPU usage',R+dict_rsi['re_cpu_Interrupt'][3]+N])
                


            #IDLE CPU    
                if int_conv(dict_rsi['re_cpu_Idle'][0]) < 30:
                    mytable.add_row(['Master RE0 5 Sec Idle CPU',R+dict_rsi['re_cpu_Idle'][0]+N])
                else:
                    mytable.add_row(['Master RE0 5 Sec Idle CPU',dict_rsi['re_cpu_Idle'][0]])
            
                if int_conv(dict_rsi['re_cpu_Idle'][1]) < 30:
                    mytable.add_row(['Master RE0 1 Min Idle CPU',R+dict_rsi['re_cpu_Idle'][1]+N])
                else:
                    mytable.add_row(['Master RE0 1 Min Idle CPU',dict_rsi['re_cpu_Idle'][1]])
            
                if int_conv(dict_rsi['re_cpu_Idle'][2]) < 30:
                    mytable.add_row(['Master RE0 5 Min Idle CPU',R+dict_rsi['re_cpu_Idle'][2]+N])
                else:
                    mytable.add_row(['Master RE0 5 Min Idle CPU',dict_rsi['re_cpu_Idle'][2]])
            
                if int_conv(dict_rsi['re_cpu_Idle'][3]) < 30:
                    mytable.add_row(['Master RE0 15 Min Idle CPU',R+dict_rsi['re_cpu_Idle'][3]+N])
                else:
                    mytable.add_row(['Master RE0 15 Min Idle CPU',dict_rsi['re_cpu_Idle'][3]])
            
        
        #Display FPC 
        if len(dict_rsi['fpc']) > 1 and FPC_info_temp != []:
            if len(FPC_info_temp) == 10:
                i = 0
                #print(dict_rsi['fpc_info_temp'])
                #print(dict_rsi['fpc_info_slot'])
                for member in dict_rsi['fpc_info_slot']:
                    mytable.add_row(['Online FPC','FPC'+str(member)])
                    # mytable.add_row([member+' Start time',dict_rsi['re_refpc_starttime'][i+2]])
                    #mytable.add_row([member+' Uptime',dict_rsi['re_refpc_uptime'][i+2]])
                    #i+=1
                    mytable.add_row(['FPC'+str(member)+' '+'Temperature',dict_rsi['fpc_info_temp'][i]])
                    mytable.add_row(['FPC'+str(member)+' '+'Total CPU',dict_rsi['fpc_info_cpu_total'][i]])
                    mytable.add_row(['FPC'+str(member)+' '+'Interrupt CPU',dict_rsi['fpc_info_cpu_intrp'][i]])
                    mytable.add_row(['FPC'+str(member)+' '+'1 min CPU',dict_rsi['fpc_info_1min'][i]])
                    mytable.add_row(['FPC'+str(member)+' '+'5 min CPU',dict_rsi['fpc_info_5min'][i]])
                    mytable.add_row(['FPC'+str(member)+' '+'15min CPU',dict_rsi['fpc_info_15min'][i]])
                    mytable.add_row(['FPC'+str(member)+' '+'DRAM',dict_rsi['fpc_info_dram'][i]])
                    mytable.add_row(['FPC'+str(member)+' '+'HEAP',dict_rsi['fpc_info_heap'][i]])
                    mytable.add_row(['FPC'+str(member)+' '+'BUFFER',dict_rsi['fpc_info_buf'][i]])
                    i+=1
        elif len(dict_rsi['fpc']) > 1 and FPC_info_temp == []:
            pass
        else:
            mytable.add_row(['Online FPC','FPC '+str(dict_rsi['fpc'][0])])
            mytable.add_row(['FPC0 Start time',dict_rsi['re_refpc_starttime'][1]])
            mytable.add_row(['FPC0 Uptime',dict_rsi['re_refpc_uptime'][1]])
        
        #Display Failed Hardware 
        if len(dict_rsi['hw_component']) >= 1:  
            i = 1
            for hw in dict_rsi['hw_component']:         
                mytable.add_row(['Failed Harware Component'+str(i),R+hw+N])
                i = i + 1
        else:
            mytable.add_row(['Hardware Components','All HW components are OK'])

        #display PFE level drops
        pfe_sw_flag = 0
        if int_conv(dict_rsi['pfe_sw_input_cntrl_drops']) != 0:
            pfe_sw_flag = 1
            mytable.add_row(['PFE Software input control plane drops',dict_rsi['pfe_sw_input_cntrl_drops']])
        if int_conv(dict_rsi['pfe_sw_input_high_drops']) != 0:
            pfe_sw_flag = 1
            mytable.add_row(['PFE Software input high drops',dict_rsi['pfe_sw_input_high_drops']])
        if int_conv(dict_rsi['pfe_sw_input_medium_drops']) != 0:
            pfe_sw_flag = 1
            mytable.add_row(['PFE Software input medium drops',dict_rsi['pfe_sw_input_medium_drops']])
        if int_conv(dict_rsi['pfe_sw_input_low_drops']) != 0:
            pfe_sw_flag = 1
            mytable.add_row(['PFE Software input low drops',dict_rsi['pfe_sw_input_low_drops']])
        if int_conv(dict_rsi['pfe_sw_output_drops']) != 0:
            pfe_sw_flag = 1
            mytable.add_row(['PFE Software output drops',dict_rsi['pfe_sw_output_drops']])
        if pfe_sw_flag == 0:
            mytable.add_row(['PFE Software control/input/output drops','No PFE Software Drops'])
        
        if int_conv(dict_rsi['pfe_hw_input_drops']) != 0:
            mytable.add_row(['PFE Hardware input drops',dict_rsi['pfe_hw_input_drops']])
        else:
            mytable.add_row(['PFE Hardware input drops','No PFE Hardware Input Drops'])

        mytable.add_row(['PFE HW Timeout',dict_rsi['pfe_timeout']])
        if dict_rsi.get('pfe_trun_key') != None:
            mytable.add_row(['PFE HW Truncated key',dict_rsi['pfe_trun_key']])
        mytable.add_row(['PFE HW  Bits to test',dict_rsi['pfe_bits_test']])
        mytable.add_row(['PFE HW Data error ',dict_rsi['pfe_data_err']])
        if dict_rsi.get('pfe_tcp_hdr_len_err') != None:
            mytable.add_row(['PFE HW TCP header length error',dict_rsi['pfe_tcp_hdr_len_err']])
        mytable.add_row(['PFE HW Stack underflow',dict_rsi['pfe_stk_undr_flow']])
        mytable.add_row(['PFE HW Stack overflow',dict_rsi['pfe_stk_ovr_flow']])
        mytable.add_row(['PFE HW Normal discard',dict_rsi['pfe_nrml_discard']])
        mytable.add_row(['PFE HW Extended discard',dict_rsi['pfe_ext_discard']])
        mytable.add_row(['PFE HW Invalid interface',dict_rsi['pfe_inv_int']])
        mytable.add_row(['PFE HW Info cell drops',dict_rsi['pfe_info_cell_drop']])
        mytable.add_row(['PFE HW Fabric drops',dict_rsi['pfe_fab_drop']])
        #print(mytable)
        print(mytable.get_string(title="HEALTH CHECK FROM RSI FILE:"+' '+RSI))

files_list = os.listdir()
files = [files for files in files_list if os.path.isfile(files)] #list comprehension to collect only files except directory
#get RSI from the files available in the current directory

RSI = list()
for i in files:
    #print(i)
    #print(type(RSI_file))
#Checking for swap file and skip it if present        
    if re.match(".*[R|r][S|s][I|i].*swp|.*gz|.*zip|.*\.py|.*\.sh",i):
        continue
        #RSI = i
    if re.match('.*[R|r][S|s][I|i].*|.*support-info.*|.*support_info.*',i):
            #print("Removing"+RSI)
            #os.remove(RSI)
         RSI.append(i)


if RSI == []:
    print("No uncompressed RSI File available in the folder")
    exit(1)


for rsi in RSI:
    obj1 = healthcheck(rsi)

    obj1.pvhcu(rsi)
