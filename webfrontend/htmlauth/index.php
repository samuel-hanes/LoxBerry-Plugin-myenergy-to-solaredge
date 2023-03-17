<?php
require_once "loxberry_web.php";
require_once "Config/Lite.php";

// This will read your language files to the array $L
$L = LBSystem::readlanguage("language.ini");
$template_title = ucfirst($lbpplugindir);
$helplink = $L['HELP.LINK'];
$helptemplate = "#";

LBWeb::lbheader($template_title, $helplink, $helptemplate);

if ($_POST){
	// Get values from form
	$api_key = $_POST['api_key'];
	$serial = $_POST['serial'];
	$ms_port = $_POST['ms_port'];
	$in_database = $_POST['in_database'];
  $in_measurement = $_POST['in_measurement'];
  $in_server = $_POST['in_server'];
  $in_port = $_POST['in_port'];
  $in_user = $_POST['in_user'];
  $in_pwd = $_POST['in_pwd'];
	
	// Write new config file
	$cfg = new Config_Lite("$lbpconfigdir/plugin.cfg",LOCK_EX,INI_SCANNER_RAW);
	$cfg->setQuoteStrings(False);
	$cfg->set("MYENERGI","API_KEY",$api_key);
	$cfg->set("MYENERGI","SERIAL",$serial);
	$cfg->set("MINISERVER","PORT",$ms_port);
  // Influxdb values
  $cfg->set("INFLUXDB","DATABASE",$in_database);
  $cfg->set("INFLUXDB","MEASUREMENT",$in_measurement);
  $cfg->set("INFLUXDB","SERVER",$in_server);
  $cfg->set("INFLUXDB","PORT",$in_port);
  $cfg->set("INFLUXDB","USERNAME",$in_user);
  $cfg->set("INFLUXDB","PASSWORD",$in_pwd);
	
	$cfg->save();
}
else {
	// Get values from config file
	$cfg = new Config_Lite("$lbpconfigdir/plugin.cfg",LOCK_EX,INI_SCANNER_RAW);
	$api_key = $cfg['MYENERGI']['API_KEY'];
	$serial = $cfg['MYENERGI']['SERIAL'];
	$ms_port = $cfg['MINISERVER']['PORT'];
	$in_database = $cfg['INFLUXDB']['DATABASE'];
	$in_measurement = $cfg['INFLUXDB']['MEASUREMENT'];
  $in_server = $cfg['INFLUXDB']['SERVER'];
	$in_port = $cfg['INFLUXDB']['PORT'];
	$in_user = $cfg['INFLUXDB']['USERNAME'];
	$in_pwd = $cfg['INFLUXDB']['PASSWORD'];
}

// This is the main area for your plugin
?>
<style>
.divTable{
    display: table;
    width: 100%;
}
.divTableRow {
    display: table-row;
}
.divTableHeading {
    background-color: #EEE;
    display: table-header-group;
}
.divTableCell, .divTableHead {
    border: 0px dotted #999999;
    display: table-cell;
    padding: 3px 10px;
    vertical-align: middle;
}
.divTableBody {
    display: table-row-group;
}
</style>
<h2><?=$L['TEXT.GREETING']?></h2>

<form method="post" data-ajax="false" name="main_form" id="main_form" action="./index.php">
        <div class="divTable">
            <div class="divTableBody">
                <div class="divTableRow">
                    <div class="divTableCell"><h3><?=$L['TEXT.API'].' '.$L['TEXT.SETTINGS']?></h3></div>
                </div>
                <div class="divTableRow">
									<div class="divTableCell" style="width:25%"><?=$L['TEXT.API_KEY']?></div>
									<div class="divTableCell"><input type="text" name="api_key" id="api_key" value="<?=$api_key?>"></div>
									<div class="divTableCell" style="width:25%"><span class="hint"><?=$L['HELP.API']?></span></div>
                </div>
                <div class="divTableRow">
									<div class="divTableCell"><?=$L['TEXT.SERIAL']?></div>
									<div class="divTableCell"><input type="number" name="serial" id="serial" value="<?=$serial?>"></div>
									<div class="divTableCell"><?=$L['HELP.SERIAL']?></div>
                </div>
                
                <div class="divTableRow">
									<div class="divTableCell"><h3><?=$L['TEXT.SRV'].' '.$L['TEXT.SETTINGS']?></h3></div>
                </div>
                <div class="divTableRow">
									<div class="divTableCell"><?=$L['TEXT.PORT']?></div>
									<div class="divTableCell"><input type="number" name="ms_port" id="ms_port" min="1025" max="65535" value="<?=$ms_port?>" data-validation-rule="special:number-min-max-value:1025:65535"></div>
									<div class="divTableCell"><?=$L['HELP.PORT']?></div>
                </div>
                
                <div class="divTableRow">
                  <div class="divTableCell"><h3><?=$L['TEXT.INFLUXB'].' '.$L['TEXT.SETTINGS']?></h3></div>
                </div>
                <div class="divTableRow">
                  <div class="divTableCell"><?=$L['TEXT.DATABASE']?></div>
                  <div class="divTableCell"><input type="text" name="in_database" id="in_database" value="<?=$in_database?>"></div>
                  <div class="divTableCell"><?=$L['HELP.DATABASE']?></div>
                </div>
                <div class="divTableRow">
                  <div class="divTableCell"><?=$L['TEXT.MEASUREMENT']?></div>
                  <div class="divTableCell"><input type="text" name="in_measurement" id="in_measurement" value="<?=$in_measurement?>"></div>
                  <div class="divTableCell"><?=$L['HELP.MEASUREMENT']?></div>
                </div>
                <div class="divTableRow">
                  <div class="divTableCell"><?=$L['TEXT.SERVER']?></div>
                  <div class="divTableCell"><input type="text" name="in_server" id="in_server" value="<?=$in_server?>"></div>
                  <div class="divTableCell"><?=$L['HELP.SERVER']?></div>
                </div>
                <div class="divTableRow">
                  <div class="divTableCell"><?=$L['TEXT.PORT']?></div>
                  <div class="divTableCell"><input type="number" name="in_port" id="in_port" min="1025" max="65535" value="<?=$in_port?>" data-validation-rule="special:number-min-max-value:1025:65535"></div>
                  <div class="divTableCell"><?=$L['HELP.PORT']?></div>
                </div>
                <div class="divTableRow">
                  <div class="divTableCell"><?=$L['TEXT.USER']?></div>
                  <div class="divTableCell"><input type="text" name="in_user" id="in_user" value="<?=$in_user?>"></div>
                  <div class="divTableCell"><?=$L['HELP.USER']?></div>
                </div>
                <div class="divTableRow">
                  <div class="divTableCell"><?=$L['TEXT.PWD']?></div>
                  <div class="divTableCell"><input type="password" name="in_pwd" id="in_pwd" value="<?=$in_pwd?>"></div>
                  <div class="divTableCell"><?=$L['HELP.PWD']?></div>
                </div>
                
								<div class="divTableRow">
									<div class="divTableCell">&nbsp;</div>
									<div class="divTableCell"><input type="submit" id="do" value="<?=$L['TEXT.SAVE']?>" data-mini="true"></div>
									<div class="divTableCell"><a id="btnlogs" data-role="button" href="/admin/system/tools/logfile.cgi?logfile=plugins/myenergi/myenergi.log&header=html&format=template" target="_blank" data-inline="true" data-mini="true" data-icon="action"><?=$L['TEXT.LOGFILE']?></a></div>
                </div>
            </div>
        </div>
</form>

<script>
$('#main_form').validate();

$( document ).ready(function()
{
    validate_enable('#ms_port');
    validate_enable('#in_port');
});
</script>

<?php
// Finally print the footer
LBWeb::lbfooter();
?>
