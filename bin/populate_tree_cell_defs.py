# Parse the .xml config file and create the appropriate data structures that contain the info needed for cell defs.
#
import sys
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5 import QtCore

def populate_tree_cell_defs(cell_def_tab):
    print("=======================  populate_tree_cell_defs(): ======================= ")
    print("    cell_def_tab.param_d = ",cell_def_tab.param_d)
    cell_def_tab.master_custom_varname.clear()

    debug_print = True

    uep = cell_def_tab.xml_root.find(".//cell_definitions")
    if uep:
        cell_def_tab.tree.clear()
        idx = 0
        for cell_def in uep:
            cell_def_tab.new_cell_def_count += 1
            # print(cell_def.attrib['name'])
            cell_def_name = cell_def.attrib['name']
            if idx == 0:
                cell_def_0th = cell_def_name
                cell_def_tab.live_phagocytosis_celltype = cell_def_0th 
                cell_def_tab.attack_rate_celltype = cell_def_0th 
                cell_def_tab.fusion_rate_celltype = cell_def_0th 
                cell_def_tab.transformation_rate_celltype = cell_def_0th 

            cell_def_tab.param_d[cell_def_name] = {}
            cell_def_tab.param_d[cell_def_name]['ID'] = cell_def.attrib['ID']  # e.g., "0"
            # cell_def_tab.param_d[cell_def_name]["name"] = cell_def_name
            cell_def_tab.current_cell_def = cell_def_name  # do this for the callback methods?

            cellname = QTreeWidgetItem([cell_def_name])
            cellname.setFlags(cellname.flags() | QtCore.Qt.ItemIsEditable)
            cell_def_tab.tree.insertTopLevelItem(idx,cellname)
            if idx == 0:  # select the 1st (0th) entry
                cell_def_tab.tree.setCurrentItem(cellname)

            idx += 1

            # Now fill the param dict for each substrate and the Qt widget values for the 0th

            if debug_print:
                print("\n===== populate_tree():  cycle")

            cycle_path = ".//cell_definition[" + str(idx) + "]//phenotype//cycle"
            cycle_code = int(uep.find(cycle_path).attrib['code'])
            if debug_print:
                print(" >> cycle_path=",cycle_path)
                print("   cycle code=",cycle_code)

            # NOTE: we don't seem to use 3 or 4
            # static const int advanced_Ki67_cycle_model= 0;
            # static const int basic_Ki67_cycle_model=1;
            # static const int flow_cytometry_cycle_model=2;
            # static const int live_apoptotic_cycle_model=3;
            # static const int total_cells_cycle_model=4;
            # static const int live_cells_cycle_model = 5; 
            # static const int flow_cytometry_separated_cycle_model = 6; 
            # static const int cycling_quiescent_model = 7; 

            # cell_def_tab.cycle_dropdown.addItem("live cells")  # 5
            # cell_def_tab.cycle_dropdown.addItem("basic Ki67")  # 1
            # cell_def_tab.cycle_dropdown.addItem("advanced Ki67")  # 0
            # cell_def_tab.cycle_dropdown.addItem("flow cytometry")  # 2
            # cell_def_tab.cycle_dropdown.addItem("flow cytometry separated")  # 6
            # cell_def_tab.cycle_dropdown.addItem("cycling quiescent")  # 7

            if cycle_code == 0:
                cell_def_tab.cycle_dropdown.setCurrentIndex(2)
                cell_def_tab.param_d[cell_def_name]['cycle'] = 'advanced Ki67'
            elif cycle_code == 1:
                cell_def_tab.cycle_dropdown.setCurrentIndex(1)
                cell_def_tab.param_d[cell_def_name]['cycle'] = 'basic Ki67'
            elif cycle_code == 2:
                cell_def_tab.cycle_dropdown.setCurrentIndex(3)
                cell_def_tab.param_d[cell_def_name]['cycle'] = 'flow cytometry'
            elif cycle_code == 5:
                cell_def_tab.cycle_dropdown.setCurrentIndex(0)
                cell_def_tab.param_d[cell_def_name]['cycle'] = 'live cells'
            elif cycle_code == 6:
                cell_def_tab.cycle_dropdown.setCurrentIndex(4)
                cell_def_tab.param_d[cell_def_name]['cycle'] = 'flow cytometry separated'
            elif cycle_code == 7:
                cell_def_tab.cycle_dropdown.setCurrentIndex(5)
                cell_def_tab.param_d[cell_def_name]['cycle'] = 'cycling quiescent'

            cell_def_tab.param_d[cell_def_name]['cycle_choice_idx'] = cell_def_tab.cycle_dropdown.currentIndex()

        # rwh: We only use cycle code=5 or 6 in ALL sample projs?!
            # <cell_definition name="cargo cell" ID="2" visible="true">
            # 	<phenotype>
            # 		<cycle code="5" name="live">  
            # 			<phase_transition_rates units="1/min"> 
            # 				<rate start_index="0" end_index="0" fixed_duration="false">0.0</rate>
            # 			</phase_transition_rates>

            # <cycle code="6" name="Flow cytometry model (separated)">  
            # 	<phase_transition_rates units="1/min"> 
            # 		<rate start_index="0" end_index="1" fixed_duration="false">0</rate>
            # 		<rate start_index="1" end_index="2" fixed_duration="true">0.00208333</rate>
            # 		<rate start_index="2" end_index="3" fixed_duration="true">0.00416667</rate>
            # 		<rate start_index="3" end_index="0" fixed_duration="true">0.0166667</rate>


            #  transition rates: set default values for all params
            default_sval = '0.0'
            cell_def_tab.param_d[cell_def_name]['cycle_live_trate00'] = default_sval

            cell_def_tab.param_d[cell_def_name]['cycle_Ki67_trate01'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_Ki67_trate10'] = default_sval

            cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_trate01'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_trate12'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_trate20'] = default_sval

            cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_trate01'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_trate12'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_trate20'] = default_sval

            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_trate01'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_trate12'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_trate23'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_trate30'] = default_sval

            cell_def_tab.param_d[cell_def_name]['cycle_quiescent_trate01'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_quiescent_trate10'] = default_sval


            #  transition rates: set default values for all "fixed_duration" checkboxes
            default_bval = False
            cell_def_tab.param_d[cell_def_name]['cycle_live_trate00_fixed'] = default_bval

            cell_def_tab.param_d[cell_def_name]['cycle_Ki67_trate01_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_Ki67_trate10_fixed'] = default_bval

            cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_trate01_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_trate12_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_trate20_fixed'] = default_bval

            cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_trate01_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_trate12_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_trate20_fixed'] = default_bval

            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_trate01_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_trate12_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_trate23_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_trate30_fixed'] = default_bval

            cell_def_tab.param_d[cell_def_name]['cycle_quiescent_trate01_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_quiescent_trate10_fixed'] = default_bval

            phase_transition_path = cycle_path + "//phase_transition_rates"
            if debug_print:
                print(' >> phase_transition_path ')
            pt_uep = uep.find(phase_transition_path)
            if pt_uep:
                cell_def_tab.cycle_rb1.setChecked(True)
                cell_def_tab.param_d[cell_def_name]['cycle_duration_flag'] = False
                cell_def_tab.cycle_duration_flag = False
                cell_def_tab.customize_cycle_choices()

                for rate in pt_uep: 
                    if debug_print:
                        print(rate)
                    # print("start_index=",rate.attrib["start_index"])
                    # We only use cycle code=5 or 6 in ALL sample projs?

                    # if cycle_code == 0: #'advanced Ki67'
                    # elif cycle_code == 1: # 'basic Ki67'
                    # elif cycle_code == 2: # 'flow cytometry'
                    # elif cycle_code == 5: # 'live cells'
                    # elif cycle_code == 6: # 'flow cytometry separated'
                    # elif cycle_code == 7: # 'cycling quiescent'

                    sval = rate.text
                    if (rate.attrib['start_index'] == "0"): 
                        if (rate.attrib['end_index'] == "0"): #  Must be 'live'
                            if debug_print:
                                print('--  cycle_live_trate00',  sval)
                            cell_def_tab.param_d[cell_def_name]['cycle_live_trate00'] = rate.text
                            if (rate.attrib['fixed_duration'].lower() == "true"): 
                                cell_def_tab.param_d[cell_def_name]['cycle_live_trate00_fixed'] = True
                        elif (rate.attrib['end_index'] == "1"): 
                            if cycle_code == 0: #'advanced Ki67'
                                cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_trate01'] = sval
                                if (rate.attrib['fixed_duration'].lower() == "true"): 
                                    cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_trate01_fixed'] = True
                            elif cycle_code == 1: # 'basic Ki67'
                                cell_def_tab.param_d[cell_def_name]['cycle_Ki67_trate01'] = sval
                                if (rate.attrib['fixed_duration'].lower() == "true"): 
                                    cell_def_tab.param_d[cell_def_name]['cycle_Ki67_trate01_fixed'] = True
                            elif cycle_code == 2: # 'flow cytometry'
                                cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_trate01'] = sval
                                if (rate.attrib['fixed_duration'].lower() == "true"): 
                                    cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_trate01_fixed'] = True
                            elif cycle_code == 6: # 'flow cytometry separated'
                                cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_trate01'] = sval
                                if (rate.attrib['fixed_duration'].lower() == "true"): 
                                    cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_trate01_fixed'] = True
                            elif cycle_code == 7: # 'cycling quiescent'
                                cell_def_tab.param_d[cell_def_name]['cycle_quiescent_trate01'] = sval
                                if (rate.attrib['fixed_duration'].lower() == "true"): 
                                    cell_def_tab.param_d[cell_def_name]['cycle_quiescent_trate01_fixed'] = True

                    elif (rate.attrib['start_index'] == "1"):
                        if (rate.attrib['end_index'] == "0"):
                            if cycle_code == 1: # 'basic Ki67'
                                cell_def_tab.param_d[cell_def_name]['cycle_Ki67_trate10'] = sval
                                if (rate.attrib['fixed_duration'].lower() == "true"): 
                                    cell_def_tab.param_d[cell_def_name]['cycle_Ki67_trate10_fixed'] = True
                            elif cycle_code == 7: # 'cycling quiescent'
                                cell_def_tab.param_d[cell_def_name]['cycle_quiescent_trate10'] = sval
                                if (rate.attrib['fixed_duration'].lower() == "true"): 
                                    cell_def_tab.param_d[cell_def_name]['cycle_quiescent_trate10_fixed'] = True
                        elif (rate.attrib['end_index'] == "2"):
                            if cycle_code == 0: #'advanced Ki67'
                                cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_trate12'] = sval
                                if (rate.attrib['fixed_duration'].lower() == "true"): 
                                    cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_trate12_fixed'] = True
                            elif cycle_code == 2: # 'flow cytometry'
                                cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_trate12'] = sval
                                if (rate.attrib['fixed_duration'].lower() == "true"): 
                                    cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_trate12_fixed'] = True
                            elif cycle_code == 6: # 'flow cytometry separated'
                                cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_trate12'] = sval
                                if (rate.attrib['fixed_duration'].lower() == "true"): 
                                    cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_trate12_fixed'] = True
                            elif cycle_code == 7: # 'cycling quiescent'
                                cell_def_tab.param_d[cell_def_name]['cycle_quiescent_trate12'] = sval
                                if (rate.attrib['fixed_duration'].lower() == "true"): 
                                    cell_def_tab.param_d[cell_def_name]['cycle_quiescent_trate12_fixed'] = True

                    elif (rate.attrib['start_index'] == "2"):
                        if (rate.attrib['end_index'] == "0"):
                            if cycle_code == 0: #'advanced Ki67'
                                cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_trate20'] = sval
                                if (rate.attrib['fixed_duration'].lower() == "true"): 
                                    cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_trate20_fixed'] = True
                            elif cycle_code == 2: # 'flow cytometry'
                                cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_trate20'] = sval
                                if (rate.attrib['fixed_duration'].lower() == "true"): 
                                    cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_trate20_fixed'] = True

                        elif (rate.attrib['end_index'] == "3"):
                            # if cycle_code == 6: # 'flow cytometry separated'
                            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_trate23'] = sval
                            if (rate.attrib['fixed_duration'].lower() == "true"): 
                                cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_trate23_fixed'] = True

                    elif (rate.attrib['start_index'] == "3") and (rate.attrib['end_index'] == "0"):
                        # cell_def_tab.cycle_flowcytosep_trate30.setText(rate.text)
                        cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_trate30'] = rate.text
                        if (rate.attrib['fixed_duration'].lower() == "true"): 
                            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_trate30_fixed'] = True


            # template.xml:
            # <cycle code="6" name="Flow cytometry model (separated)">  
            #     <phase_durations units="min"> 
            #         <duration index="0" fixed_duration="false">300.0</duration>
            #         <duration index="1" fixed_duration="true">480</duration>
            #         <duration index="2" fixed_duration="true">240</duration>
            #         <duration index="3" fixed_duration="true">60</duration>
            #     </phase_durations>
            #
            # cell_def_tab.phase0_duration = QLineEdit()
            default_sval = '0.0'

            cell_def_tab.param_d[cell_def_name]['cycle_live_duration00'] = default_sval

            cell_def_tab.param_d[cell_def_name]['cycle_Ki67_duration01'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_Ki67_duration10'] = default_sval

            cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_duration01'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_duration12'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_duration20'] = default_sval

            cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_duration01'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_duration12'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_duration20'] = default_sval

            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration00'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration01'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration12'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration23'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration30'] = default_sval

            cell_def_tab.param_d[cell_def_name]['cycle_quiescent_duration01'] = default_sval
            cell_def_tab.param_d[cell_def_name]['cycle_quiescent_duration10'] = default_sval

            #  duration: set default values for all "fixed_duration" checkboxes
            default_bval = False
            cell_def_tab.param_d[cell_def_name]['cycle_live_duration00_fixed'] = default_bval

            cell_def_tab.param_d[cell_def_name]['cycle_Ki67_duration01_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_Ki67_duration10_fixed'] = default_bval

            cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_duration01_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_duration12_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_duration20_fixed'] = default_bval

            cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_duration01_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_duration12_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_duration20_fixed'] = default_bval

            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration01_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration12_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration23_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration30_fixed'] = default_bval

            cell_def_tab.param_d[cell_def_name]['cycle_quiescent_duration01_fixed'] = default_bval
            cell_def_tab.param_d[cell_def_name]['cycle_quiescent_duration10_fixed'] = default_bval

            phase_durations_path = cycle_path + "//phase_durations"
            if debug_print:
                print(' >> phase_durations_path =',phase_durations_path )
            pd_uep = uep.find(phase_durations_path)
            if debug_print:
                print(' >> pd_uep =',pd_uep )
            if pd_uep:
                cell_def_tab.cycle_rb2.setChecked(True)
                cell_def_tab.param_d[cell_def_name]['cycle_duration_flag'] = True
                cell_def_tab.cycle_duration_flag = True   # rwh: TODO - why do this??
                cell_def_tab.customize_cycle_choices()

            # if cycle_code == 0: #'advanced Ki67'
            # elif cycle_code == 1: # 'basic Ki67'
            # elif cycle_code == 2: # 'flow cytometry'
            # elif cycle_code == 5: # 'live cells'
            # elif cycle_code == 6: # 'flow cytometry separated'
            # elif cycle_code == 7: # 'cycling quiescent'

                for pd in pd_uep:   # phase_duration
                    if debug_print:
                        print(pd)
                    # print("index=",pd.attrib["index"])
                    sval = pd.text

                    if (pd.attrib['index'] == "0"): 
                        if cycle_code == 0: #'advanced Ki67'
                            cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_duration01'] = sval
                            if (pd.attrib['fixed_duration'].lower() == "true"): 
                                cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_duration01_fixed'] = True
                        elif cycle_code == 1: # 'basic Ki67'
                            cell_def_tab.param_d[cell_def_name]['cycle_Ki67_duration01'] = sval
                            if (pd.attrib['fixed_duration'].lower() == "true"): 
                                cell_def_tab.param_d[cell_def_name]['cycle_Ki67_duration01_fixed'] = True
                        elif cycle_code == 2: # 'flow cytometry'
                            cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_duration01'] = sval
                            if (pd.attrib['fixed_duration'].lower() == "true"): 
                                cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_duration01_fixed'] = True
                        elif cycle_code == 5: # 'live'
                            cell_def_tab.param_d[cell_def_name]['cycle_live_duration00'] = sval
                            if (pd.attrib['fixed_duration'].lower() == "true"): 
                                cell_def_tab.param_d[cell_def_name]['cycle_live_duration00_fixed'] = True
                        elif cycle_code == 6: # 'flow cytometry separated'
                            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration01'] = sval
                            if (pd.attrib['fixed_duration'].lower() == "true"): 
                                cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration01_fixed'] = True
                        elif cycle_code == 7: # 'cycling quiescent'
                            cell_def_tab.param_d[cell_def_name]['cycle_quiescent_duration01'] = sval
                            if (pd.attrib['fixed_duration'].lower() == "true"): 
                                cell_def_tab.param_d[cell_def_name]['cycle_quiescent_duration01_fixed'] = True

                    elif (pd.attrib['index'] == "1"):
                        if cycle_code == 0: #'advanced Ki67'
                            cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_duration12'] = sval
                            if (pd.attrib['fixed_duration'].lower() == "true"): 
                                cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_duration12_fixed'] = True
                        elif cycle_code == 1: #'basic Ki67'
                            cell_def_tab.param_d[cell_def_name]['cycle_Ki67_duration10'] = sval
                            if (pd.attrib['fixed_duration'].lower() == "true"): 
                                cell_def_tab.param_d[cell_def_name]['cycle_Ki67_duration10_fixed'] = True
                        elif cycle_code == 2: # 'flow cytometry'
                            cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_duration12'] = sval
                            if (pd.attrib['fixed_duration'].lower() == "true"): 
                                cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_duration12_fixed'] = True
                        elif cycle_code == 6: # 'flow cytometry separated'
                            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration12'] = sval
                            if (pd.attrib['fixed_duration'].lower() == "true"): 
                                cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration12_fixed'] = True
                        elif cycle_code == 7: # 'cycling quiescent'
                            cell_def_tab.param_d[cell_def_name]['cycle_quiescent_duration10'] = sval
                            if (pd.attrib['fixed_duration'].lower() == "true"): 
                                cell_def_tab.param_d[cell_def_name]['cycle_quiescent_duration10_fixed'] = True

                    elif (pd.attrib['index'] == "2"):
                        if cycle_code == 0: #'advanced Ki67'
                            cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_duration20'] = sval
                            if (pd.attrib['fixed_duration'].lower() == "true"): 
                                cell_def_tab.param_d[cell_def_name]['cycle_advancedKi67_duration20_fixed'] = True
                        elif cycle_code == 2: # 'flow cytometry'
                            cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_duration20'] = sval
                            if (pd.attrib['fixed_duration'].lower() == "true"): 
                                cell_def_tab.param_d[cell_def_name]['cycle_flowcyto_duration20_fixed'] = True
                        elif cycle_code == 6: # 'flow cytometry separated'
                            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration23'] = sval
                            if (pd.attrib['fixed_duration'].lower() == "true"): 
                                cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration23_fixed'] = True

                    elif (pd.attrib['index'] == "3"):
                        cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration30'] = sval
                        if (pd.attrib['fixed_duration'].lower() == "true"): 
                            cell_def_tab.param_d[cell_def_name]['cycle_flowcytosep_duration30_fixed'] = True


            # rf. microenv:
            # cell_def_tab.cell_type_name.setText(var.attrib['name'])
            # cell_def_tab.diffusion_coef.setText(vp[0].find('.//diffusion_coefficient').text)

            # ------------------ cell_definition: default
            # ---------  cycle (live)
            # cell_def_tab.float0.value = float(uep.find('.//cell_definition[1]//phenotype//cycle//phase_transition_rates//rate[1]').text)

            cell_def_tab.param_d[cell_def_name]['cycle_live_duration00'] = default_sval

            # ---------  death 
            if debug_print:
                print("\n===== populate_tree():  death")

                    #------ using transition_rates
                    # <death> 
                    #   <model code="100" name="apoptosis"> 
                        #     <death_rate units="1/min">0</death_rate>  
                        #     <phase_transition_rates units="1/min">
                        #         <rate start_index="0" end_index="1" fixed_duration="true">0.00193798</rate>
                        #     </phase_transition_rates>
                        #     <parameters>
                        #         <unlysed_fluid_change_rate units="1/min">0.05</unlysed_fluid_change_rate>
                        #         <lysed_fluid_change_rate units="1/min">0</lysed_fluid_change_rate>
                        #         <cytoplasmic_biomass_change_rate units="1/min">1.66667e-02</cytoplasmic_biomass_change_rate>
                        #         <nuclear_biomass_change_rate units="1/min">5.83333e-03</nuclear_biomass_change_rate>
                        #         <calcification_rate units="1/min">0</calcification_rate>
                        #         <relative_rupture_volume units="dimensionless">2.0</relative_rupture_volume>
                        #     </parameters>
                        # </model> 
                    #   <model code="101" name="necrosis">

                    #------ using durations
                    # <death>  
                    # 	<model code="100" name="apoptosis"> 
                    # 		<death_rate units="1/min">5.1e-05</death_rate>
                    # 		<phase_durations units="min">
                    # 			<duration index="0" fixed_duration="true">511</duration>
                    # 		</phase_durations>
                    # 		<parameters>
                    # 			<unlysed_fluid_change_rate units="1/min">0.01</unlysed_fluid_change_rate>
                    # 			<lysed_fluid_change_rate units="1/min">1.e-99</lysed_fluid_change_rate>
                    # 			<cytoplasmic_biomass_change_rate units="1/min">1.61e-02</cytoplasmic_biomass_change_rate>
                    # 			<nuclear_biomass_change_rate units="1/min">5.81e-03</nuclear_biomass_change_rate>
                    # 			<calcification_rate units="1/min">0</calcification_rate>
                    # 			<relative_rupture_volume units="dimensionless">2.1</relative_rupture_volume>
                    # 		</parameters>
                    # 	</model> 

                    # 	<model code="101" name="necrosis">
                    # 		<death_rate units="1/min">0.1</death_rate>
                    # 		<phase_durations units="min">
                    # 			<duration index="0" fixed_duration="true">0.1</duration>
                    # 			<duration index="1" fixed_duration="true">86400.1</duration>
                    # 		</phase_durations>


            death_path = ".//cell_definition[" + str(idx) + "]//phenotype//death//"

            cell_def_tab.param_d[cell_def_name]['apoptosis_duration_flag'] = False
            cell_def_tab.param_d[cell_def_name]["apoptosis_phase0_duration"] = "0.0"
            cell_def_tab.param_d[cell_def_name]["apoptosis_phase0_fixed"] = False
            cell_def_tab.param_d[cell_def_name]["apoptosis_trate01"] = "0.0"
            cell_def_tab.param_d[cell_def_name]["apoptosis_trate01_fixed"] = False

            cell_def_tab.param_d[cell_def_name]['necrosis_duration_flag'] = False
            cell_def_tab.param_d[cell_def_name]["necrosis_phase0_duration"] = "0.0"
            cell_def_tab.param_d[cell_def_name]["necrosis_phase0_fixed"] = False
            cell_def_tab.param_d[cell_def_name]["necrosis_phase1_duration"] = "0.0"
            cell_def_tab.param_d[cell_def_name]["necrosis_phase1_fixed"] = False
            cell_def_tab.param_d[cell_def_name]["necrosis_trate01"] = "0.0"
            cell_def_tab.param_d[cell_def_name]["necrosis_trate01_fixed"] = False
            cell_def_tab.param_d[cell_def_name]["necrosis_trate12"] = "0.0"
            cell_def_tab.param_d[cell_def_name]["necrosis_trate12_fixed"] = False

            # uep = cell_def_tab.xml_root.find('.//microenvironment_setup')  # find unique entry point
            death_uep = uep.find(".//cell_definition[" + str(idx) + "]//phenotype//death")
            if debug_print:
                print('death_uep=',death_uep)

            for death_model in death_uep.findall('model'):
                if "apoptosis" in death_model.attrib["name"].lower():
                    if debug_print:
                        print("-------- parsing apoptosis!")
                    cell_def_tab.param_d[cell_def_name]["apoptosis_death_rate"] = death_model.find('death_rate').text

                    # 	<model code="100" name="apoptosis"> 
                    # 		<death_rate units="1/min">5.1e-05</death_rate>
                    # 		<phase_durations units="min">
                    # 			<duration index="0" fixed_duration="true">511</duration>
                    # 		</phase_durations>
                    # 		<parameters>
                    # 			<unlysed_fluid_change_rate units="1/min">0.01</unlysed_fluid_change_rate>
                    pd_uep = death_model.find("phase_durations")
                    if pd_uep is not None:
                        if debug_print:
                            print(' >> pd_uep =',pd_uep )
                        cell_def_tab.param_d[cell_def_name]['apoptosis_duration_flag'] = True
                        # cell_def_tab.apoptosis_rb2.setChecked(True)  # duration

                        for pd in pd_uep:   # <duration index= ... >
                            if debug_print:
                                print(pd)
                                print("index=",pd.attrib["index"])
                            if  pd.attrib['index'] == "0":
                                cell_def_tab.param_d[cell_def_name]["apoptosis_phase0_duration"] = pd.text
                                if  pd.attrib['fixed_duration'].lower() == "true":
                                    cell_def_tab.param_d[cell_def_name]["apoptosis_phase0_fixed"] = True
                                else:
                                    cell_def_tab.param_d[cell_def_name]["apoptosis_phase0_fixed"] = False

                    else:  #  transition rates
                        #     <phase_transition_rates units="1/min">
                        #         <rate start_index="0" end_index="1" fixed_duration="true">0.00193798</rate>
                        #     </phase_transition_rates>
                        tr_uep = death_model.find("phase_transition_rates")
                        if tr_uep is not None:
                            if debug_print:
                                print(' >> tr_uep =',tr_uep )
                            # cell_def_tab.apoptosis_rb1.setChecked(True)  # trate01

                            for tr in tr_uep:   # <duration index= ... >
                                if debug_print:
                                    print(tr)
                                    print("start_index=",tr.attrib["start_index"])

                                if  tr.attrib['start_index'] == "0":
                                    cell_def_tab.param_d[cell_def_name]["apoptosis_trate01"] = tr.text
                                    if  tr.attrib['fixed_duration'].lower() == "true":
                                        cell_def_tab.param_d[cell_def_name]["apoptosis_trate01_fixed"] = True
                                    else:
                                        cell_def_tab.param_d[cell_def_name]["apoptosis_trate01_fixed"] = False

                    # apoptosis_params_path = apoptosis_path + "parameters//"
                    params_uep = death_model.find("parameters")
                    # apoptosis_params_path = apoptosis_path + "parameters//"

                    # cell_def_tab.param_d[cell_def_name]["apoptosis_unlysed_rate"] = params_uep.find("unlysed_fluid_change_rate").text
                    cell_def_tab.param_d[cell_def_name]["apoptosis_unlysed_rate"] = params_uep.find("unlysed_fluid_change_rate").text
                    cell_def_tab.param_d[cell_def_name]["apoptosis_lysed_rate"] = params_uep.find("lysed_fluid_change_rate").text
                    cell_def_tab.param_d[cell_def_name]["apoptosis_cyto_rate"] = params_uep.find("cytoplasmic_biomass_change_rate").text
                    cell_def_tab.param_d[cell_def_name]["apoptosis_nuclear_rate"] = params_uep.find("nuclear_biomass_change_rate").text
                    cell_def_tab.param_d[cell_def_name]["apoptosis_calcif_rate"] = params_uep.find("calcification_rate").text
                    cell_def_tab.param_d[cell_def_name]["apoptosis_rel_rupture_volume"] = params_uep.find("relative_rupture_volume").text

            #--------------
            # necrosis_params_path = necrosis_path + "parameters//"
                elif "necrosis" in death_model.attrib["name"].lower():
                    if debug_print:
                        print("-------- parsing necrosis!")
                    cell_def_tab.param_d[cell_def_name]["necrosis_death_rate"] = death_model.find('death_rate').text

                    pd_uep = death_model.find("phase_durations")
                    if pd_uep is not None:
                        if debug_print:
                            print(' >> pd_uep =',pd_uep )
                        # cell_def_tab.necrosis_rb2.setChecked(True)  # duration
                        cell_def_tab.param_d[cell_def_name]['necrosis_duration_flag'] = True

                        for pd in pd_uep:   # <duration index= ... >
                            if debug_print:
                                print(pd)
                                print("index=",pd.attrib["index"])
                            if  pd.attrib['index'] == "0":
                                cell_def_tab.param_d[cell_def_name]["necrosis_phase0_duration"] = pd.text
                                if  pd.attrib['fixed_duration'].lower() == "true":
                                    cell_def_tab.param_d[cell_def_name]["necrosis_phase0_fixed"] = True
                                else:
                                    cell_def_tab.param_d[cell_def_name]["necrosis_phase0_fixed"] = False
                            elif  pd.attrib['index'] == "1":
                                cell_def_tab.param_d[cell_def_name]["necrosis_phase1_duration"] = pd.text
                                if  pd.attrib['fixed_duration'].lower() == "true":
                                    cell_def_tab.param_d[cell_def_name]["necrosis_phase1_fixed"] = True
                                else:
                                    cell_def_tab.param_d[cell_def_name]["necrosis_phase1_fixed"] = False

                    else:  # transition rates
                        #     <phase_transition_rates units="1/min">
                        #         <rate start_index="0" end_index="1" fixed_duration="true">0.00193798</rate>
                        #     </phase_transition_rates>
                        tr_uep = death_model.find("phase_transition_rates")
                        if tr_uep is not None:
                            if debug_print:
                                print(' >> tr_uep =',tr_uep )
                            # cell_def_tab.necrosis_rb1.setChecked(True)  
                            for tr in tr_uep:  # transition rate 
                                if debug_print:
                                    print(tr)
                                    print("start_index=",tr.attrib["start_index"])
                                if  tr.attrib['start_index'] == "0":
                                    rate = float(tr.text)
                                    if debug_print:
                                        print(" --- transition rate (float) = ",rate)
                                    if abs(rate) < 1.e-6:
                                        dval = 9.e99
                                    else:
                                        dval = rate * 60.0
                                    if debug_print:
                                        print(" --- transition rate (float) = ",rate)
                                    # cell_def_tab.param_d[cell_def_name]["necrosis_phase0_duration"] = tr.text
                                    cell_def_tab.param_d[cell_def_name]["necrosis_phase0_duration"] = str(dval)
                                    if  tr.attrib['fixed_duration'].lower() == "true":
                                        cell_def_tab.param_d[cell_def_name]["necrosis_phase0_fixed"] = True
                                    else:
                                        cell_def_tab.param_d[cell_def_name]["necrosis_phase0_fixed"] = False
                                elif  tr.attrib['start_index'] == "1":
                                    cell_def_tab.param_d[cell_def_name]["necrosis_phase1_duration"] = tr.text
                                    if  tr.attrib['fixed_duration'].lower() == "true":
                                        cell_def_tab.param_d[cell_def_name]["necrosis_phase1_fixed"] = True
                                    else:
                                        cell_def_tab.param_d[cell_def_name]["necrosis_phase1_fixed"] = False


                    params_uep = death_model.find("parameters")

                    cell_def_tab.param_d[cell_def_name]["necrosis_unlysed_rate"] = params_uep.find("unlysed_fluid_change_rate").text
                    cell_def_tab.param_d[cell_def_name]["necrosis_lysed_rate"] = params_uep.find("lysed_fluid_change_rate").text
                    cell_def_tab.param_d[cell_def_name]["necrosis_cyto_rate"] = params_uep.find("cytoplasmic_biomass_change_rate").text
                    cell_def_tab.param_d[cell_def_name]["necrosis_nuclear_rate"] = params_uep.find("nuclear_biomass_change_rate").text
                    cell_def_tab.param_d[cell_def_name]["necrosis_calcif_rate"] = params_uep.find("calcification_rate").text
                    cell_def_tab.param_d[cell_def_name]["necrosis_rel_rupture_rate"] = params_uep.find("relative_rupture_volume").text


            # # ---------  volume 
                    # <volume>  
                    # 	<total units="micron^3">2494</total>
                    # 	<fluid_fraction units="dimensionless">0.75</fluid_fraction>
                    # 	<nuclear units="micron^3">540</nuclear>
                        
                    # 	<fluid_change_rate units="1/min">0.05</fluid_change_rate>
                    # 	<cytoplasmic_biomass_change_rate units="1/min">0.0045</cytoplasmic_biomass_change_rate>
                    # 	<nuclear_biomass_change_rate units="1/min">0.0055</nuclear_biomass_change_rate>
                        
                    # 	<calcified_fraction units="dimensionless">0</calcified_fraction>
                    # 	<calcification_rate units="1/min">0</calcification_rate>
                        
                    # 	<relative_rupture_volume units="dimensionless">2.0</relative_rupture_volume>

            volume_path = ".//cell_definition[" + str(idx) + "]//phenotype//volume//"
            if debug_print:
                print('volume_path=',volume_path)

            # cell_def_tab.volume_total.setText(uep.find(volume_path+"total").text)
            # cell_def_tab.volume_fluid_fraction.setText(uep.find(volume_path+"fluid_fraction").text)
            # cell_def_tab.volume_nuclear.setText(uep.find(volume_path+"nuclear").text)
            # cell_def_tab.volume_fluid_change_rate.setText(uep.find(volume_path+"fluid_change_rate").text)
            # cell_def_tab.volume_cytoplasmic_biomass_change_rate.setText(uep.find(volume_path+"cytoplasmic_biomass_change_rate").text)
            # cell_def_tab.volume_nuclear_biomass_change_rate.setText(uep.find(volume_path+"nuclear_biomass_change_rate").text)
            # cell_def_tab.volume_calcified_fraction.setText(uep.find(volume_path+"calcified_fraction").text)
            # cell_def_tab.volume_calcification_rate.setText(uep.find(volume_path+"calcification_rate").text)
            # cell_def_tab.relative_rupture_volume.setText(uep.find(volume_path+"relative_rupture_volume").text)

            cell_def_tab.param_d[cell_def_name]["volume_total"] = uep.find(volume_path+"total").text
            cell_def_tab.param_d[cell_def_name]["volume_fluid_fraction"] = uep.find(volume_path+"fluid_fraction").text
            cell_def_tab.param_d[cell_def_name]["volume_nuclear"] = uep.find(volume_path+"nuclear").text
            cell_def_tab.param_d[cell_def_name]["volume_fluid_change_rate"] = uep.find(volume_path+"fluid_change_rate").text
            cell_def_tab.param_d[cell_def_name]["volume_cytoplasmic_rate"] = uep.find(volume_path+"cytoplasmic_biomass_change_rate").text
            cell_def_tab.param_d[cell_def_name]["volume_nuclear_rate"] = uep.find(volume_path+"nuclear_biomass_change_rate").text
            cell_def_tab.param_d[cell_def_name]["volume_calcif_fraction"] = uep.find(volume_path+"calcified_fraction").text
            cell_def_tab.param_d[cell_def_name]["volume_calcif_rate"] = uep.find(volume_path+"calcification_rate").text
            cell_def_tab.param_d[cell_def_name]["volume_rel_rupture_vol"] = uep.find(volume_path+"relative_rupture_volume").text


            # # ---------  mechanics 
            if debug_print:
                print("\n===== populate_tree():  mechanics")
                    # <mechanics> 
                    # 	<cell_cell_adhesion_strength units="micron/min">0.4</cell_cell_adhesion_strength>
                    # 	<cell_cell_repulsion_strength units="micron/min">10.0</cell_cell_repulsion_strength>
                    # 	<relative_maximum_adhesion_distance units="dimensionless">1.25</relative_maximum_adhesion_distance>
                        
                    # 	<options>
                    # 		<set_relative_equilibrium_distance enabled="false" units="dimensionless">1.8</set_relative_equilibrium_distance>
                    # 		<set_absolute_equilibrium_distance enabled="false" units="micron">15.12</set_absolute_equilibrium_distance>
                    # 	</options>

            mechanics_path = ".//cell_definition[" + str(idx) + "]//phenotype//mechanics//"
            if debug_print:
                print('mechanics_path=',mechanics_path)

            # cell_def_tab.cell_cell_adhesion_strength.setText(uep.find(mechanics_path+"cell_cell_adhesion_strength").text)
            # cell_def_tab.cell_cell_repulsion_strength.setText(uep.find(mechanics_path+"cell_cell_repulsion_strength").text)
            val =  uep.find(mechanics_path+"cell_cell_adhesion_strength").text
            cell_def_tab.param_d[cell_def_name]["mechanics_adhesion"] = val

            val =  uep.find(mechanics_path+"cell_cell_repulsion_strength").text
            cell_def_tab.param_d[cell_def_name]["mechanics_repulsion"] = val

            val =  uep.find(mechanics_path+"relative_maximum_adhesion_distance").text
            cell_def_tab.param_d[cell_def_name]["mechanics_adhesion_distance"] = val

            # cell_def_tab.relative_maximum_adhesion_distance.setText(uep.find(mechanics_path+"relative_maximum_adhesion_distance").text)

            #----------
            cell_adhesion_affinities_path = ".//cell_definition[" + str(idx) + "]//phenotype//mechanics//cell_adhesion_affinities"
            if debug_print:
                print("---- cell_interactions_path= ",cell_adhesion_affinities_path)
            # motility_options_path = ".//cell_definition[" + str(idx) + "]//phenotype//motility//options//"
            # motility_chemotaxis_path = motility_options_path + "chemotaxis//"
            # if uep.find(motility_chemotaxis_path) is None:

            # if uep.find(motility_advanced_chemotaxis_path) is None:
            cap = uep.find(cell_adhesion_affinities_path)
            if cap is None:
                # print("---- no cell_adhesion_affinities_path found. Setting to default values")
                print("---- No cell_adhesion_affinities_path found. Setting to default.")

                # for var in cap.findall('cell_adhesion_affinity'):
                #     print(" --> ",var.attrib['name'])
                #     name = var.attrib['name']

                cell_def_tab.param_d[cell_def_name]["cell_adhesion_affinity"] = {}
                # print("\nFor now, you need to manually enter these into your .xml\n")
                # sys.exit(-1)

                cds_uep = cell_def_tab.xml_root.find('.//cell_definitions')  # find unique entry point
                if cds_uep is None:
                    print("---- Error: cell_definitions is not defined.")
                    sys.exit(-1)

                sval = '1.0'
                for var in cds_uep.findall('cell_definition'):
                    print(" --> ",var.attrib['name'])
                    name = var.attrib['name']
                    cell_def_tab.param_d[cell_def_name]["cell_adhesion_affinity"][name] = sval

            else:
                print("---- found cell_adhesion_affinities_path:")
                cell_def_tab.param_d[cell_def_name]["cell_adhesion_affinity"] = {}
                    # <cell_adhesion_affinities>
	  				# 	<cell_adhesion_affinity name="bacteria">1</cell_adhesion_affinity> 
	  				# 	<cell_adhesion_affinity name="blood vessel">1</cell_adhesion_affinity> 
                for var in cap.findall('cell_adhesion_affinity'):
                    celltype_name = var.attrib['name']
                    val = var.text
                    # print(celltype_name,val)
                    cell_def_tab.param_d[cell_def_name]["cell_adhesion_affinity"][celltype_name] = val
                    print("--> ",cell_def_tab.param_d[cell_def_name]["cell_adhesion_affinity"])


                # cell_def_tab.param_d[cell_def_name]["cell_adhesion_affinity"] = {}

            # print("---> ",cell_def_tab.param_d[cell_def_name]["cell_adhesion_affinity"])

            #----------
            mechanics_options_path = ".//cell_definition[" + str(idx) + "]//phenotype//mechanics//options//"
            # cell_def_tab.set_relative_equilibrium_distance.setText(uep.find(mechanics_options_path+"set_relative_equilibrium_distance").text)

            # cell_def_tab.set_absolute_equilibrium_distance.setText(uep.find(mechanics_options_path+"set_absolute_equilibrium_distance").text)

            val =  uep.find(mechanics_options_path+"set_relative_equilibrium_distance").text
            cell_def_tab.param_d[cell_def_name]["mechanics_relative_equilibrium_distance"] = val

            val =  uep.find(mechanics_options_path+"set_absolute_equilibrium_distance").text
            cell_def_tab.param_d[cell_def_name]["mechanics_absolute_equilibrium_distance"] = val

            if uep.find(mechanics_options_path+"set_relative_equilibrium_distance").attrib['enabled'].lower() == 'true':
                cell_def_tab.param_d[cell_def_name]["mechanics_relative_equilibrium_distance_enabled"] = True
            else:
                cell_def_tab.param_d[cell_def_name]["mechanics_relative_equilibrium_distance_enabled"] = False

            if uep.find(mechanics_options_path+"set_absolute_equilibrium_distance").attrib['enabled'].lower() == 'true':
                cell_def_tab.param_d[cell_def_name]["mechanics_absolute_equilibrium_distance_enabled"] = True
            else:
                cell_def_tab.param_d[cell_def_name]["mechanics_absolute_equilibrium_distance_enabled"] = False


            # # ---------  motility 
            if debug_print:
                print("\n===== populate_tree():  motility")
                    # <motility>  
                    # 	<speed units="micron/min">5.0</speed>
                    # 	<persistence_time units="min">5.0</persistence_time>
                    # 	<migration_bias units="dimensionless">0.5</migration_bias>
                        
                    # 	<options>
                    # 		<enabled>true</enabled>
                    # 		<use_2D>true</use_2D>
                    # 		<chemotaxis>
                    # 			<enabled>false</enabled>
                    # 			<substrate>director signal</substrate>
                    # 			<direction>1</direction>
                    # 		</chemotaxis>
                    # 	</options>

            motility_path = ".//cell_definition[" + str(idx) + "]//phenotype//motility//"
            if debug_print:
                print('motility_path=',motility_path)

            val = uep.find(motility_path+"speed").text
            cell_def_tab.param_d[cell_def_name]["speed"] = val

            val = uep.find(motility_path+"persistence_time").text
            cell_def_tab.param_d[cell_def_name]["persistence_time"] = val

            val = uep.find(motility_path+"migration_bias").text
            cell_def_tab.param_d[cell_def_name]["migration_bias"] = val

            motility_options_path = ".//cell_definition[" + str(idx) + "]//phenotype//motility//options//"

            # print(' motility options enabled', uep.find(motility_options_path +'enabled').text)
            if uep.find(motility_options_path +'enabled').text.lower() == 'true':
                cell_def_tab.param_d[cell_def_name]["motility_enabled"] = True
            else:
                cell_def_tab.param_d[cell_def_name]["motility_enabled"] = False

            if uep.find(motility_options_path +'use_2D').text.lower() == 'true':
                cell_def_tab.param_d[cell_def_name]["motility_use_2D"] = True
            else:
                cell_def_tab.param_d[cell_def_name]["motility_use_2D"] = False

                    # 		<chemotaxis>
                    # 			<enabled>false</enabled>
                    # 			<substrate>director signal</substrate>
                    # 			<direction>1</direction>
                    # 		</chemotaxis>
            motility_chemotaxis_path = motility_options_path + "chemotaxis//"
            if uep.find(motility_chemotaxis_path) is None:
                cell_def_tab.param_d[cell_def_name]["motility_chemotaxis"] = False
                cell_def_tab.param_d[cell_def_name]["motility_chemotaxis_substrate"] = ""
                cell_def_tab.param_d[cell_def_name]["motility_chemotaxis_towards"] = True
            else:
                if uep.find(motility_chemotaxis_path +'enabled').text.lower() == 'true':
                    cell_def_tab.param_d[cell_def_name]["motility_chemotaxis"] = True
                else:
                    cell_def_tab.param_d[cell_def_name]["motility_chemotaxis"] = False

                val = uep.find(motility_chemotaxis_path +'substrate').text
                cell_def_tab.param_d[cell_def_name]["motility_chemotaxis_substrate"] = val

                val = uep.find(motility_chemotaxis_path +'direction').text
                if val == '1':
                    cell_def_tab.param_d[cell_def_name]["motility_chemotaxis_towards"] = True
                else:
                    cell_def_tab.param_d[cell_def_name]["motility_chemotaxis_towards"] = False

        #   <advanced_chemotaxis>
        #     <enabled>false</enabled>
        #     <normalize_each_gradient>false</normalize_each_gradient>
        #     <chemotactic_sensitivities>
        #       <chemotactic_sensitivity substrate="resource">0</chemotactic_sensitivity> 
        #       <chemotactic_sensitivity substrate="toxin">0</chemotactic_sensitivity> 
        #       <chemotactic_sensitivity substrate="quorum">0</chemotactic_sensitivity> 
        #       <chemotactic_sensitivity substrate="pro-inflammatory">0</chemotactic_sensitivity> 
        #       <chemotactic_sensitivity substrate="debris">0</chemotactic_sensitivity> 
        #     </chemotactic_sensitivities>
        #   </advanced_chemotaxis>
            motility_advanced_chemotaxis_path = motility_options_path + "advanced_chemotaxis//"
            # motility_advanced_chemotaxis_path = motility_options_path + "advanced_chemotaxis"
            print(motility_advanced_chemotaxis_path)

            # Just initialize sensitivities to default value (0) for all substrates
            cell_def_tab.param_d[cell_def_name]['chemotactic_sensitivity'] = {}
            uep_microenv = cell_def_tab.xml_root.find(".//microenvironment_setup")
            for subelm in uep_microenv.findall('variable'):
                substrate_name = subelm.attrib['name']
                cell_def_tab.param_d[cell_def_name]["chemotactic_sensitivity"][substrate_name] = '0.0'
            print("chemotactic_sensitivity= ",cell_def_tab.param_d[cell_def_name]["chemotactic_sensitivity"])
            # sys.exit(-1)

            if uep.find(motility_advanced_chemotaxis_path) is None:  # advanced_chemotaxis not present in .xml
                print("---- no motility_advanced_chemotaxis_path found. Setting to default values")
                cell_def_tab.param_d[cell_def_name]["motility_advanced_chemotaxis"] = False
                cell_def_tab.param_d[cell_def_name]["motility_advanced_chemotaxis_substrate"] = ""
                # cell_def_tab.param_d[cell_def_name]['chemotactic_sensitivity'] = {}
                # print("---- cell_def_tab.substrate_list= ",cell_def_tab.substrate_list)
                # for substrate in cell_def_tab.substrate_list:
                #     print("---- setting chemotactic_sensitivity= 0.0 for ",substrate)
                #     cell_def_tab.param_d[cell_def_name]["chemotactic_sensitivity"][substrate] = '0.0'
                cell_def_tab.param_d[cell_def_name]["motility_advanced_chemotaxis_normalize_grad"] = False
                # sys.exit(-1)

            else:    # advanced_chemotaxis IS present in .xml
                if uep.find(motility_advanced_chemotaxis_path +'enabled').text.lower() == 'true':
                    cell_def_tab.param_d[cell_def_name]["motility_advanced_chemotaxis"] = True
                else:
                    cell_def_tab.param_d[cell_def_name]["motility_advanced_chemotaxis"] = False

                # val = uep.find(motility_chemotaxis_path +'substrate').text
                cell_def_tab.param_d[cell_def_name]["motility_advanced_chemotaxis_substrate"] = "foobar"
                # cell_def_tab.param_d[cell_def_name]["motility_advanced_chemotaxis_substrate"] = None

                if uep.find(motility_advanced_chemotaxis_path +'normalize_each_gradient').text.lower() == 'true':
                    cell_def_tab.param_d[cell_def_name]["motility_advanced_chemotaxis_normalize_grad"] = True
                else:
                    cell_def_tab.param_d[cell_def_name]["motility_advanced_chemotaxis_normalize_grad"] = False

                cell_def_tab.param_d[cell_def_name]['chemotactic_sensitivity'] = {}
                for substrate in cell_def_tab.substrate_list:
                    # cell_def_tab.chemotactic_sensitivity_dict[substrate] = 0.0
                    cell_def_tab.param_d[cell_def_name]["chemotactic_sensitivity"][substrate] = '0.0'

                #-----
                sensitivity_path = motility_options_path + "advanced_chemotaxis//chemotactic_sensitivities"
                print(sensitivity_path)
                # sys.exit(-1)
                if uep.find(sensitivity_path) is None:
                    print("---- chemotactic_sensitivities not found. Set to defaults (0). ")
                    # sys.exit(-1)
        #       <chemotactic_sensitivity substrate="resource">0</chemotactic_sensitivity> 
                else:
                    # cell_def_tab.param_d[cell_def_name]['chemotactic_sensitivity'] = {}
                    if debug_print:
                        print("---- found chemotactic_sensitivities: ",uep.find(sensitivity_path))
                    for subelm in uep.find(sensitivity_path).findall('chemotactic_sensitivity'):
                        subname = subelm.attrib['substrate']
                        subval = subelm.text # float?
                        if debug_print:
                            print('subelm=',subelm)
                            print(" chemotactic_sensitivity--> ",subname,' = ',subval)
                        # cell_def_tab.chemotactic_sensitivity_dict[subname] = subval
                        cell_def_tab.param_d[cell_def_name]['chemotactic_sensitivity'][subname] = subval
                if debug_print:
                    # print("sensitivity_dict = ",cell_def_tab.chemotactic_sensitivity_dict)
                    print(cell_def_tab.param_d[cell_def_name]['chemotactic_sensitivity'])

                # val = uep.find(motility_chemotaxis_path +'substrate').text
                # cell_def_tab.param_d[cell_def_name]["motility_chemotaxis_substrate"] = val

                # val = uep.find(motility_chemotaxis_path +'direction').text
                # if val == '1':
                #     cell_def_tab.param_d[cell_def_name]["motility_chemotaxis_towards"] = True
                # else:
                #     cell_def_tab.param_d[cell_def_name]["motility_chemotaxis_towards"] = False

            # sys.exit(-1)


            # # ---------  secretion 
            if debug_print:
                print("\n===== populate_tree():  secretion")

            # <substrate name="virus">
            #     <secretion_rate units="1/min">0</secretion_rate>
            #     <secretion_target units="substrate density">1</secretion_target>
            #     <uptake_rate units="1/min">10</uptake_rate>
            #     <net_export_rate units="total substrate/min">0</net_export_rate> 
            # </substrate> 

            secretion_path = ".//cell_definition[" + str(idx) + "]//phenotype//secretion//"
            if debug_print:
                print('secretion_path =',secretion_path)
            secretion_sub1_path = ".//cell_definition[" + str(idx) + "]//phenotype//secretion//substrate[1]//"

            uep_secretion = cell_def_tab.xml_root.find(".//cell_definitions//cell_definition[" + str(idx) + "]//phenotype//secretion")
            if debug_print:
                print('uep_secretion = ',uep_secretion )
            

            # e.g.: param_d["cancer cell"]["oxygen"]["secretion_rate"] = 0.0
            # or,   param_d["cancer cell"]["oxygen"]["secretion_rate"] = 0.0
            # or,   param_d["cancer cell"]["secretion"] = {"oxygen" : { "secretion_rate" : 42.0 } }
            cell_def_tab.param_d[cell_def_name]["secretion"] = {}  # a dict for these params

            # Initialize (set to 0.0) all substrates' secretion params
            # val = "0.0"
            # print('----- populate_tree: cell_def_tab.substrate_list = ',cell_def_tab.substrate_list )
            # for substrate_name in cell_def_tab.substrate_list:
            #     print('----- populate_tree: substrate_name = ',substrate_name )
            #     cell_def_tab.param_d[cell_def_name]["secretion"][substrate_name]["secretion_rate"] = val
            #     cell_def_tab.param_d[cell_def_name]["secretion"][substrate_name]["secretion_target"] = val
            #     cell_def_tab.param_d[cell_def_name]["secretion"][substrate_name]["uptake_rate"] = val
            #     cell_def_tab.param_d[cell_def_name]["secretion"][substrate_name]["net_export_rate"] = val
            # foo = 1/0


            jdx = 0
            for sub in uep_secretion.findall('substrate'):
                substrate_name = sub.attrib['name']
                if jdx == 0:
                    cell_def_tab.current_secretion_substrate = substrate_name

                if debug_print:
                    print(jdx,") -- secretion substrate = ",substrate_name)
                # cell_def_tab.param_d[cell_def_tab.current_cell_def]["secretion"][substrate_name]["secretion_rate"] = {}
                cell_def_tab.param_d[cell_def_name]["secretion"][substrate_name] = {}

                tptr = sub.find("secretion_rate")
                if tptr is not None:
                    val = tptr.text
                else:
                    val = "0.0"
                cell_def_tab.param_d[cell_def_name]["secretion"][substrate_name]["secretion_rate"] = val
                # print(cell_def_tab.param_d[cell_def_name]["secretion"][substrate_name] )

                tptr = sub.find("secretion_target")
                if tptr is not None:
                    val = tptr.text
                else:
                    val = "0.0"
                cell_def_tab.param_d[cell_def_name]["secretion"][substrate_name]["secretion_target"] = val

                tptr = sub.find("uptake_rate")
                if tptr is not None:
                    val = tptr.text
                else:
                    val = "0.0"
                cell_def_tab.param_d[cell_def_name]["secretion"][substrate_name]["uptake_rate"] = val

                tptr = sub.find("net_export_rate")
                if tptr is not None:
                    val = tptr.text
                else:
                    val = "0.0"
                cell_def_tab.param_d[cell_def_name]["secretion"][substrate_name]["net_export_rate"] = val

                jdx += 1

            if debug_print:
                print("------ done parsing secretion:")
            # print("------ cell_def_tab.param_d = ",cell_def_tab.param_d)
            

            # # --------- cell_interactions  
            print("\n===== populate_tree():  cell_interactions")
            # <cell_interactions>
            #  <dead_phagocytosis_rate units="1/min">0</dead_phagocytosis_rate>
            #  <live_phagocytosis_rates>
            #     <phagocytosis_rate name="bacteria" units="1/min">0</phagocytosis_rate>
            #     <phagocytosis_rate name="blood vessel" units="1/min">0</phagocytosis_rate>

            # cell_def_tab.dead_phagocytosis_rate.setText(cell_def_tab.param_d[cdname]["dead_phagocytosis_rate"])
            # cell_interactions_path = cell_def_tab.xml_root.find(".//cell_definitions//cell_definition[" + str(idx) + "]//phenotype//cell_interactions")
            cell_interactions_path = ".//cell_definition[" + str(idx) + "]//phenotype//cell_interactions"
            if debug_print:
                print("---- cell_interactions_path= ",cell_interactions_path)
            # motility_options_path = ".//cell_definition[" + str(idx) + "]//phenotype//motility//options//"
            # motility_chemotaxis_path = motility_options_path + "chemotaxis//"
            # if uep.find(motility_chemotaxis_path) is None:

            # if uep.find(motility_advanced_chemotaxis_path) is None:
            cep = uep.find(cell_interactions_path)
            if cep is None:
                print("---- no cell_interactions found. Setting to default values")
                # print("---- no cell_interactions found.")
                # print("\nFor now, you need to manually enter these (and cell_transformations) into your .xml \n")
                # sys.exit(-1)

                cell_def_tab.param_d[cell_def_name]["dead_phagocytosis_rate"] = '0.0'
                cell_def_tab.param_d[cell_def_name]["damage_rate"] = '0.0'

                cell_def_tab.param_d[cell_def_name]["live_phagocytosis_rate"] = {}
                cell_def_tab.param_d[cell_def_name]["attack_rate"] = {}
                cell_def_tab.param_d[cell_def_name]["fusion_rate"] = {}

                cds_uep = cell_def_tab.xml_root.find('.//cell_definitions')  # find unique entry point
                if cds_uep is None:
                    print("---- Error: cell_definitions is not defined.")
                    sys.exit(-1)

                sval = '0.0'
                for var in cds_uep.findall('cell_definition'):
                    print(" --> ",var.attrib['name'])
                    name = var.attrib['name']
                    cell_def_tab.param_d[cell_def_name]["live_phagocytosis_rate"][name] = sval
                    cell_def_tab.param_d[cell_def_name]["attack_rate"][name] = sval
                    cell_def_tab.param_d[cell_def_name]["fusion_rate"][name] = sval
            else:
                print("---- found cell_interactions:")
                val = cep.find("dead_phagocytosis_rate").text
                cell_def_tab.param_d[cell_def_name]["dead_phagocytosis_rate"] = val

                val = cep.find("damage_rate").text
                cell_def_tab.param_d[cell_def_name]["damage_rate"] = val

                # <cell_interactions>
                #   <dead_phagocytosis_rate units="1/min">91.0</dead_phagocytosis_rate>
                #   <live_phagocytosis_rates>
                #     <phagocytosis_rate name="bacteria" units="1/min">91.1</phagocytosis_rate>
                #     <phagocytosis_rate name="blood vessel" units="1/min">91.2</phagocytosis_rate>
                # uep_lpr = cep.find(cell_interactions_path + "//live_phagocytosis_rates")
                # uep_lpr = cep.find(cell_interactions_path + "//live_phagocytosis_rates")
                uep2 = uep.find(cell_interactions_path + "//live_phagocytosis_rates")
                print("uep2= ",uep2)
                cell_def_tab.param_d[cell_def_name]["live_phagocytosis_rate"] = {}
                for pr in uep2.findall('phagocytosis_rate'):
                    celltype_name = pr.attrib['name']
                    val = pr.text
                    # print(celltype_name,val)
                    cell_def_tab.param_d[cell_def_name]["live_phagocytosis_rate"][celltype_name] = val

                uep2 = uep.find(cell_interactions_path + "//attack_rates")
                cell_def_tab.param_d[cell_def_name]["attack_rate"] = {}
                for ar in uep2.findall('attack_rate'):
                    celltype_name = ar.attrib['name']
                    val = ar.text
                    # print(celltype_name,val)
                    cell_def_tab.param_d[cell_def_name]["attack_rate"][celltype_name] = val

                uep2 = uep.find(cell_interactions_path + "//fusion_rates")
                cell_def_tab.param_d[cell_def_name]["fusion_rate"] = {}
                for ar in uep2.findall('fusion_rate'):
                    celltype_name = ar.attrib['name']
                    val = ar.text
                    # print(celltype_name,val)
                    cell_def_tab.param_d[cell_def_name]["fusion_rate"][celltype_name] = val

            if debug_print:
                # print(cell_def_tab.param_d[cell_def_name])
                print(" live_phagocytosis_rate=",cell_def_tab.param_d[cell_def_name]["live_phagocytosis_rate"])
                print(" attack_rate=",cell_def_tab.param_d[cell_def_name]["attack_rate"])
                print(" fusion_rate=",cell_def_tab.param_d[cell_def_name]["fusion_rate"])
                print("------ done parsing cell_interactions:")


            # # --------- cell_transformations  
            transformation_rates_path = ".//cell_definition[" + str(idx) + "]//phenotype//cell_transformations//transformation_rates"
            if debug_print:
                print("---- transformation_rates_path = ",transformation_rates_path)
            trp = uep.find(transformation_rates_path)
            cell_def_tab.param_d[cell_def_name]['transformation_rate'] = {}
            if trp is None:
                # print("---- No cell_transformations found.")
                # print("\nFor now, you need to manually enter these into your .xml\n")
                # sys.exit(-1)
                print("---- No cell_transformations found. Setting to default values")
                cell_def_tab.param_d[cell_def_name]['transformation_rate'] = {}

                cds_uep = cell_def_tab.xml_root.find('.//cell_definitions')  # find unique entry point
                if cds_uep is None:
                    print("---- Error: cell_definitions is not defined.")
                    sys.exit(-1)

                sval = '0.0'
                for var in cds_uep.findall('cell_definition'):
                    print(" --> ",var.attrib['name'])
                    name = var.attrib['name']
                    cell_def_tab.param_d[cell_def_name]["transformation_rate"][name] = sval
            else:
                for tr in trp.findall('transformation_rate'):
                    celltype_name = tr.attrib['name']
                    val = tr.text
                    cell_def_tab.param_d[cell_def_name]['transformation_rate'][celltype_name] = val


            if debug_print:
                print(" transformation_rate=",cell_def_tab.param_d[cell_def_name]["transformation_rate"])
                print("------ done parsing cell_transformations:")

            # sys.exit(-1)


            # # ---------  molecular 
            print("\n===== populate_tree():  molecular")


            # # ---------  intracellular 
            print("\n===== populate_tree():  intracellular")
            # <intracellular type="maboss">
            # 	<bnd_filename>./config/model_0.bnd</bnd_filename>
            # 	<cfg_filename>./config/model.cfg</cfg_filename>
            # 	<time_step>1</time_step>
            # 	<initial_values>
            # 		<initial_value node="A">1</initial_value>
            # 		<initial_value node="C">0</initial_value>
            # 	</initial_values>	
            #   <mutations>
            #       <mutation node="C">0.0</mutation>
            #   </mutations>
            #   <parameters>
            #       <parameter name="$time_scale">0.2</parameter>
            #   </parameters>
            #   <scaling>0.25</scaling>
            # </intracellular>
            intracellular_path = ".//cell_definitions//cell_definition[" + str(idx) + "]//phenotype//intracellular"
         
            uep_intracellular = cell_def_tab.xml_root.find(intracellular_path)
            cell_def_tab.param_d[cell_def_name]["intracellular"] = None

            if uep_intracellular is not None and "type" in uep_intracellular.attrib:  # also check for <intracellular />
                cell_def_tab.param_d[cell_def_name]["intracellular"] = {}
                if uep_intracellular.attrib["type"] == "maboss":
                    # --------- PhysiBoSS specific code
                    cell_def_tab.param_d[cell_def_name]["intracellular"]["type"] = "maboss" 
                    cell_def_tab.param_d[cell_def_name]["intracellular"]["bnd_filename"] = uep_intracellular.find("bnd_filename").text if uep_intracellular.find("bnd_filename") is not None else None
                    cell_def_tab.param_d[cell_def_name]["intracellular"]["cfg_filename"] = uep_intracellular.find("cfg_filename").text if uep_intracellular.find("cfg_filename") is not None else None
                    cell_def_tab.param_d[cell_def_name]["intracellular"]["time_step"] = uep_intracellular.find("time_step").text if uep_intracellular.find("time_step") is not None else "12.0"
                    cell_def_tab.param_d[cell_def_name]["intracellular"]["scaling"] = uep_intracellular.find("scaling").text if uep_intracellular.find("scaling") is not None else "1.0"
                    cell_def_tab.param_d[cell_def_name]["intracellular"]["time_stochasticity"] = uep_intracellular.find("time_stochasticity").text if uep_intracellular.find("time_stochasticity") is not None else "1.0"

                    cell_def_tab.param_d[cell_def_name]["intracellular"]["initial_values"] = []
                    uep_intracellular_iv = uep_intracellular.find("initial_values")
                    if uep_intracellular_iv is not None:
                        for initial_value in uep_intracellular_iv:
                            cell_def_tab.param_d[cell_def_name]["intracellular"]["initial_values"].append((initial_value.attrib["node"], initial_value.text))
                  
                    cell_def_tab.param_d[cell_def_name]["intracellular"]["mutants"] = []
                    uep_intracellular_mutants = uep_intracellular.find("mutations")
                    if uep_intracellular_mutants is not None:
                        for mutant in uep_intracellular_mutants:
                            cell_def_tab.param_d[cell_def_name]["intracellular"]["mutants"].append((mutant.attrib["node"], mutant.text))

                    cell_def_tab.param_d[cell_def_name]["intracellular"]["parameters"] = []
                    uep_intracellular_parameters = uep_intracellular.find("parameters")
                    if uep_intracellular_parameters is not None:
                        for parameter in uep_intracellular_parameters:
                            cell_def_tab.param_d[cell_def_name]["intracellular"]["parameters"].append((parameter.attrib["name"], parameter.text))                    

                if uep_intracellular.attrib["type"] == "roadrunner":
                    # --------- LibRR specific code
                    cell_def_tab.param_d[cell_def_name]["intracellular"]["type"] = "roadrunner"
                    cell_def_tab.param_d[cell_def_name]["intracellular"]["sbml_filename"] = uep_intracellular.find("sbml_filename").text if uep_intracellular.find("sbml_filename") is not None else None

            print("------ done parsing intracellular:")

            # # ---------  custom data 
            print("\n===== populate_tree():  custom data")
            # <custom_data>  
            # 	<receptor units="dimensionless">0.0</receptor>
            # 	<cargo_release_o2_threshold units="mmHg">10</cargo_release_o2_threshold>

            uep_custom_data = cell_def_tab.xml_root.find(".//cell_definitions//cell_definition[" + str(idx) + "]//custom_data")
            # custom_data_path = ".//cell_definition[" + str(cell_def_tab.idx_current_cell_def) + "]//custom_data//"
            print('uep_custom_data=',uep_custom_data)

            # for jdx in range(cell_def_tab.custom_data_count):
            #     cell_def_tab.custom_data_name[jdx].setText('')
            #     cell_def_tab.custom_data_value[jdx].setText('')
                

            jdx = 0
            # rwh/TODO: if we have more vars than we initially created rows for, we'll need
            # to call 'append_more_cb' for the excess.
            cell_def_tab.custom_data_count = 0
            if uep_custom_data:
                # print("--------------- populate_tree: custom_dat for cell_def_name= ",cell_def_name)
                cell_def_tab.param_d[cell_def_name]['custom_data'] = {}
                for var in uep_custom_data:
                    # print(jdx, ") ",var)
                    # val = sub.find("secretion_rate").text
                    val = var.text
                    # print("tag= ",var.tag)
                    # print("val= ",val)
                    # cell_def_tab.param_d[cell_def_name]["secretion"][substrate_name]["secretion_rate"] = val
                    cell_def_tab.param_d[cell_def_name]['custom_data'][var.tag] = val
                    if var.tag not in cell_def_tab.master_custom_varname:
                        cell_def_tab.master_custom_varname.append(var.tag)
                    cell_def_tab.custom_data_count += 1
            #     cell_def_tab.custom_data_name[jdx].setText(var.tag)
            #     print("tag=",var.tag)
            #     cell_def_tab.custom_data_value[jdx].setText(var.text)

            #     if 'units' in var.keys():
            #         cell_def_tab.custom_data_units[jdx].setText(var.attrib['units'])
            #     jdx += 1

                # print("--------- populate_tree: cell_def_tab.param_d[cell_def_name]['custom_data'] = ",cell_def_tab.param_d[cell_def_name]['custom_data'])


    cell_def_tab.current_cell_def = cell_def_0th
    cell_def_tab.tree.setCurrentItem(cell_def_tab.tree.topLevelItem(0))  # select the top (0th) item
    cell_def_tab.tree_item_clicked_cb(cell_def_tab.tree.topLevelItem(0), 0)  # and have its params shown

    # print("\n\n=======================  leaving cell_def populate_tree  ======================= ")
    # print()
    # for k in cell_def_tab.param_d.keys():
    #     print(" ===>>> ",k, " : ", cell_def_tab.param_d[k])
    #     print()