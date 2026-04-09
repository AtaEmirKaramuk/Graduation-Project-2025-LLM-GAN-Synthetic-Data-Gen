using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Security.Policy;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml.Linq;

namespace FinalProject
{
	public partial class formTestCase : Form
	{
		private readonly scriptRunner _scriptRunner;
		private readonly settingsParser _settingsParser;
		private readonly settingsFileUpdater _settingsUpdater;
		private readonly string _settingsPath;
		private readonly string _promptPath;
        string pythonProjectPath;



        public formTestCase()
		{
            InitializeComponent();
			string projectRoot = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, @"..\..\.."));
            pythonProjectPath = Path.Combine(projectRoot, "PythonScripts");
            _settingsPath = Path.Combine(pythonProjectPath, "settings.py");
            _promptPath = Path.Combine(pythonProjectPath, "TestDataProject", "generated_mode", "field_prompt.json");
            _scriptRunner = new scriptRunner(pythonProjectPath);
			_settingsParser = new settingsParser();
			cbxLLM.DropDownStyle = ComboBoxStyle.DropDownList;
			btnAutomate.Enabled = false;
			if (!string.IsNullOrEmpty(txtURL.Text) && looksLikeUrl(txtURL.Text)) btnAutomate.Enabled = true;

			try
			{
				_settingsUpdater = new settingsFileUpdater(_settingsPath, _promptPath);
				loadSettings();
				MessageBox.Show($"Successfully loaded settings from:\n{_settingsPath}");
			}
			catch (Exception ex)
			{
				MessageBox.Show($"Failed to load settings:\n{_settingsPath}\n\nError: {ex.Message}");
			}
		}

		private void loadSettings()
		{
			try
			{
				_settingsParser.LoadFromFileArgos(_settingsPath);

				int numberIndex = Int32.Parse(_settingsParser.RunNumber) - 1;

				chbxUseGPU.Checked = _settingsParser.UseGpu;
				chbxUseLLM.Checked = _settingsParser.UseZephyr;
				chbxUseDefault.Checked = _settingsParser.UseDefault;
				cbxLLM.SelectedIndex = numberIndex;
				txtURL.Text = _settingsParser.Url ?? string.Empty;

			}
			catch (Exception ex)
			{
				MessageBox.Show($"Failed to load settings: {ex.Message}\n\n" +
							  "Default settings will be used instead.",
							  "Settings Error",
							  MessageBoxButtons.OK,
							  MessageBoxIcon.Warning);
			}
		}

		private void btnSaveSettings_Click(object sender, EventArgs e)
		{
			updateSettings();
		}

		private void updateSettings()
		{
			string url = txtURL.Text.Trim();
			string numberOfLLM = cbxLLM.SelectedItem.ToString();

			if (!string.IsNullOrEmpty(url) && !looksLikeUrl(url))
			{
				MessageBox.Show("Please enter a valid URL format (e.g., http://example.com) or leave empty.");
				return;
			}


			var updater = new settingsFileUpdater(_settingsPath, _promptPath);
			updater.updateSettingsArgos(
				chbxUseGPU.Checked,
				chbxUseLLM.Checked,
				chbxUseDefault.Checked,
				numberOfLLM,
				string.IsNullOrEmpty(url) ? null : url
			);
		}

		private bool looksLikeUrl(string input)
		{
			if (string.IsNullOrWhiteSpace(input))
				return false; 

			bool hasScheme = input.StartsWith("http://", StringComparison.OrdinalIgnoreCase) ||
							input.StartsWith("https://", StringComparison.OrdinalIgnoreCase);

			bool hasDot = input.Contains(".");
			bool noSpaces = !input.Contains(" ");

			return (hasScheme && hasDot) || (noSpaces && hasDot);
		}

		private void btnCreateTestCase_Click(object sender, EventArgs e)
		{
			string url = txtURL.Text.Trim();

			updateSettings();

			bool runContextual = !string.IsNullOrEmpty(url);

			if (runContextual && !looksLikeUrl(url))
			{
				MessageBox.Show("The text doesn't look like a valid URL.\n" +
							  "Examples:\n" +
							  "- https://example.com\n" +
							  "- http://test.site\n\n" +
							  "Leave empty to run non-contextual tests.",
							  "URL Format Warning",
							  MessageBoxButtons.OK,
							  MessageBoxIcon.Warning);
				return;
			}


			try
			{
				Cursor.Current = Cursors.WaitCursor;
				btnCreateTestCase.Enabled = false;

				string scriptPath = runContextual
					? @"TestCaseGenerator\Contextual\run_all_contextual.py"
					: @"TestCaseGenerator\Non-Contextual\run_all.py";

				_scriptRunner.runScripts(pythonProjectPath, scriptPath);



			}
			catch (Exception ex)
			{
				MessageBox.Show($"Error: {ex.Message}", "Error",
							  MessageBoxButtons.OK, MessageBoxIcon.Error);
			}
			finally
			{
				btnCreateTestCase.Enabled = true;
				Cursor.Current = Cursors.Default;
			}
		}

		private void btnReturn_Click(object sender, EventArgs e)
		{
			this.Hide();
			var form = new formMain();
			form.ShowDialog();
			this.Close();
		}

		private void txtURL_TextChanged(object sender, EventArgs e)
		{
			string url = txtURL.Text;

			btnAutomate.Enabled = !string.IsNullOrEmpty(url) && looksLikeUrl(url);
		}

		private void btnAutomate_Click(object sender, EventArgs e)
		{
			string scriptPath = "auto_login_pipeline.py";
			_scriptRunner.runScripts(pythonProjectPath, scriptPath);
		}
	}
}
