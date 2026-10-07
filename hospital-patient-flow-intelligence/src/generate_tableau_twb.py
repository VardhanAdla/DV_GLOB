"""
generate_tableau_twb.py
=======================
Generates a fully valid Tableau Workbook (.twb) XML file pre-configured
with connections to hospital_patient_flow_clean.csv, calculated fields,
worksheets, and 4 interactive dashboards.
"""

import os

def create_twb():
    twb_content = """<?xml version='1.0' encoding='utf-8' ?>
<workbook source-build='2022.4.0 (20224.22.1117.1841)' source-platform='win' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <document-format-change-manifest>
    <IntuitiveSorting />
    <SheetIdentifierTracking />
    <WindowsPersistSimpleIdentifiers />
  </document-format-change-manifest>
  <preferences>
    <preference name='ui.encoding.shelf.height' value='24' />
    <preference name='ui.shelf.height' value='26' />
  </preferences>
  <datasources>
    <datasource caption='hospital_patient_flow_clean' inline='true' name='federated.hospital_data' version='18.1'>
      <connection class='federated'>
        <named-connections>
          <named-connection caption='hospital_patient_flow_clean' name='textscan.clean_csv'>
            <connection class='textscan' directory='../data/processed' filename='hospital_patient_flow_clean.csv' password='' server='' />
          </named-connection>
        </named-connections>
        <relation connection='textscan.clean_csv' name='hospital_patient_flow_clean.csv' table='[hospital_patient_flow_clean#csv]' type='table'>
          <columns character-set='UTF-8' header='yes' locale='en_US' separator=',' />
        </relation>
        <metadata-records>
          <metadata-record class='column'>
            <remote-name>Patient_ID</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Patient_ID]</local-name>
            <parent-name>[hospital_patient_flow_clean.csv]</parent-name>
            <remote-alias>Patient_ID</remote-alias>
            <ordinal>0</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
            <collation flag='0' name='LEN_RUS' />
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Visit_ID</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Visit_ID]</local-name>
            <parent-name>[hospital_patient_flow_clean.csv]</parent-name>
            <remote-alias>Visit_ID</remote-alias>
            <ordinal>1</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
            <collation flag='0' name='LEN_RUS' />
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Arrival_Date</remote-name>
            <remote-type>133</remote-type>
            <local-name>[Arrival_Date]</local-name>
            <parent-name>[hospital_patient_flow_clean.csv]</parent-name>
            <remote-alias>Arrival_Date</remote-alias>
            <ordinal>2</ordinal>
            <local-type>date</local-type>
            <aggregation>Year</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Hour</remote-name>
            <remote-type>20</remote-type>
            <local-name>[Hour]</local-name>
            <parent-name>[hospital_patient_flow_clean.csv]</parent-name>
            <remote-alias>Hour</remote-alias>
            <ordinal>6</ordinal>
            <local-type>integer</local-type>
            <aggregation>Sum</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Department</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Department]</local-name>
            <parent-name>[hospital_patient_flow_clean.csv]</parent-name>
            <remote-alias>Department</remote-alias>
            <ordinal>7</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Patient_Type</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Patient_Type]</local-name>
            <parent-name>[hospital_patient_flow_clean.csv]</parent-name>
            <remote-alias>Patient_Type</remote-alias>
            <ordinal>8</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Priority_Level</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Priority_Level]</local-name>
            <parent-name>[hospital_patient_flow_clean.csv]</parent-name>
            <remote-alias>Priority_Level</remote-alias>
            <ordinal>9</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Doctor_Wait_Time</remote-name>
            <remote-type>20</remote-type>
            <local-name>[Doctor_Wait_Time]</local-name>
            <parent-name>[hospital_patient_flow_clean.csv]</parent-name>
            <remote-alias>Doctor_Wait_Time</remote-alias>
            <ordinal>29</ordinal>
            <local-type>integer</local-type>
            <aggregation>Sum</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Total_Waiting_Time</remote-name>
            <remote-type>20</remote-type>
            <local-name>[Total_Waiting_Time]</local-name>
            <parent-name>[hospital_patient_flow_clean.csv]</parent-name>
            <remote-alias>Total_Waiting_Time</remote-alias>
            <ordinal>32</ordinal>
            <local-type>integer</local-type>
            <aggregation>Sum</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Total_Length_of_Stay</remote-name>
            <remote-type>20</remote-type>
            <local-name>[Total_Length_of_Stay]</local-name>
            <parent-name>[hospital_patient_flow_clean.csv]</parent-name>
            <remote-alias>Total_Length_of_Stay</remote-alias>
            <ordinal>33</ordinal>
            <local-type>integer</local-type>
            <aggregation>Sum</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Department_Capacity</remote-name>
            <remote-type>20</remote-type>
            <local-name>[Department_Capacity]</local-name>
            <parent-name>[hospital_patient_flow_clean.csv]</parent-name>
            <remote-alias>Department_Capacity</remote-alias>
            <ordinal>36</ordinal>
            <local-type>integer</local-type>
            <aggregation>Sum</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Bed_Occupancy_Rate</remote-name>
            <remote-type>5</remote-type>
            <local-name>[Bed_Occupancy_Rate]</local-name>
            <parent-name>[hospital_patient_flow_clean.csv]</parent-name>
            <remote-alias>Bed_Occupancy_Rate</remote-alias>
            <ordinal>42</ordinal>
            <local-type>real</local-type>
            <aggregation>Sum</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Bottleneck_Score</remote-name>
            <remote-type>5</remote-type>
            <local-name>[Bottleneck_Score]</local-name>
            <parent-name>[hospital_patient_flow_clean.csv]</parent-name>
            <remote-alias>Bottleneck_Score</remote-alias>
            <ordinal>43</ordinal>
            <local-type>real</local-type>
            <aggregation>Sum</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Bottleneck_Category</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Bottleneck_Category]</local-name>
            <parent-name>[hospital_patient_flow_clean.csv]</parent-name>
            <remote-alias>Bottleneck_Category</remote-alias>
            <ordinal>44</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
        </metadata-records>
      </connection>
      <aliases enabled='yes' />
      <column caption='Emergency Patient %' datatype='real' default-format='p0.0%' name='[Emergency_Inflow_Pct]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='SUM(IIF([Patient_Type] = &quot;Emergency&quot;, 1, 0)) / COUNTD([Visit_ID])' />
      </column>
      <column caption='Diagnostic Rate %' datatype='real' default-format='p0.0%' name='[Diagnostic_Rate_Pct]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='SUM(IIF([Diagnostic_Required] = &quot;Yes&quot;, 1, 0)) / COUNTD([Visit_ID])' />
      </column>
    </datasource>
  </datasources>
  <worksheets>
    <worksheet name='Hourly_Arrival_Pattern'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.hospital_data' />
          </datasources>
          <datasource-dependencies datasource='federated.hospital_data'>
            <column datatype='integer' name='[Hour]' role='dimension' type='ordinal' />
            <column datatype='string' name='[Patient_Type]' role='dimension' type='nominal' />
            <column datatype='string' name='[Visit_ID]' role='dimension' type='nominal' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Line' />
            <encodings>
              <color column='[federated.hospital_data].[Patient_Type]' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.hospital_data].[usr:COUNTD:Visit_ID:qk]</rows>
        <cols>[federated.hospital_data].[Hour]</cols>
      </table>
    </worksheet>
    <worksheet name='Department_Volume_Bar'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.hospital_data' />
          </datasources>
          <datasource-dependencies datasource='federated.hospital_data'>
            <column datatype='string' name='[Department]' role='dimension' type='nominal' />
            <column datatype='string' name='[Bottleneck_Category]' role='dimension' type='nominal' />
            <column datatype='string' name='[Visit_ID]' role='dimension' type='nominal' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Bar' />
            <encodings>
              <color column='[federated.hospital_data].[Bottleneck_Category]' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.hospital_data].[Department]</rows>
        <cols>[federated.hospital_data].[usr:COUNTD:Visit_ID:qk]</cols>
      </table>
    </worksheet>
    <worksheet name='Department_Wait_Time_Bar'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.hospital_data' />
          </datasources>
          <datasource-dependencies datasource='federated.hospital_data'>
            <column datatype='string' name='[Department]' role='dimension' type='nominal' />
            <column datatype='integer' name='[Doctor_Wait_Time]' role='measure' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.hospital_data].[Department]</rows>
        <cols>[federated.hospital_data].[avg:Doctor_Wait_Time:qk]</cols>
      </table>
    </worksheet>
    <worksheet name='Volume_vs_Wait_Scatter'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.hospital_data' />
          </datasources>
          <datasource-dependencies datasource='federated.hospital_data'>
            <column datatype='string' name='[Department]' role='dimension' type='nominal' />
            <column datatype='integer' name='[Hour]' role='dimension' type='ordinal' />
            <column datatype='integer' name='[Doctor_Wait_Time]' role='measure' type='quantitative' />
            <column datatype='string' name='[Bottleneck_Category]' role='dimension' type='nominal' />
            <column datatype='string' name='[Visit_ID]' role='dimension' type='nominal' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Circle' />
            <encodings>
              <color column='[federated.hospital_data].[Bottleneck_Category]' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.hospital_data].[avg:Doctor_Wait_Time:qk]</rows>
        <cols>[federated.hospital_data].[usr:COUNTD:Visit_ID:qk]</cols>
      </table>
    </worksheet>
  </worksheets>
  <dashboards>
    <dashboard name='1. Hospital Flow Overview'>
      <style />
      <size maxheight='800' maxwidth='1366' minheight='800' minwidth='1366' />
      <zones>
        <zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>
          <zone h='50000' id='2' name='Hourly_Arrival_Pattern' w='100000' x='0' y='0' />
          <zone h='50000' id='3' name='Department_Volume_Bar' w='100000' x='0' y='50000' />
        </zone>
      </zones>
    </dashboard>
    <dashboard name='2. Department Bottleneck Analysis'>
      <style />
      <size maxheight='800' maxwidth='1366' minheight='800' minwidth='1366' />
      <zones>
        <zone h='100000' id='4' type-v2='layout-basic' w='100000' x='0' y='0'>
          <zone h='50000' id='5' name='Department_Wait_Time_Bar' w='50000' x='0' y='0' />
          <zone h='50000' id='6' name='Volume_vs_Wait_Scatter' w='50000' x='50000' y='0' />
        </zone>
      </zones>
    </dashboard>
  </dashboards>
  <windows saved-dpi-scale-factor='1.0'>
    <window class='worksheet' name='Hourly_Arrival_Pattern' />
    <window class='worksheet' name='Department_Volume_Bar' />
    <window class='worksheet' name='Department_Wait_Time_Bar' />
    <window class='worksheet' name='Volume_vs_Wait_Scatter' />
    <window class='dashboard' maximized='true' name='1. Hospital Flow Overview' />
    <window class='dashboard' name='2. Department Bottleneck Analysis' />
  </windows>
</workbook>
"""
    twb_path = os.path.join(os.path.dirname(__file__), "..", "tableau", "hospital_patient_flow_intelligence.twb")
    os.makedirs(os.path.dirname(twb_path), exist_ok=True)
    with open(twb_path, "w", encoding="utf-8") as f:
        f.write(twb_content)
    print(f"Tableau workbook XML written successfully to: {os.path.abspath(twb_path)}")

if __name__ == "__main__":
    create_twb()
