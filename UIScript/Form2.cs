using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml.Linq;

namespace FinalProject
{
	public partial class formTestUser : Form
	{
		private readonly scriptRunner _scriptRunner;
		private readonly settingsParser _settingsParser;
		private readonly settingsFileUpdater _settingsUpdater;
		private readonly string _settingsPath;
		private readonly string _promptPath;
		string pythonProjectPath = @"C:\Users\guven\Documents\GitHub\FinalProject";

		public formTestUser()
		{
			InitializeComponent();
            string solutionRoot = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, @"..\..\.."));
            pythonProjectPath = Path.Combine(solutionRoot, "PythonScripts");
            _settingsPath = Path.Combine(pythonProjectPath, "settings.py");
            _promptPath = Path.Combine(pythonProjectPath, "TestDataProject", "generated_mode", "field_prompt.json");
            _scriptRunner = new scriptRunner(pythonProjectPath);
			_settingsParser = new settingsParser();
			panelLLM.Enabled = false;
			panelLLM.Visible = false;
			panelURL.Enabled = false;
			panelURL.Visible = false;
			panelPrompt.Enabled = false;
			panelPrompt.Visible = false;

			try
			{
				_settingsUpdater = new settingsFileUpdater(_settingsPath, _promptPath);
				MessageBox.Show($"Successfully loaded settings from:\n{_settingsPath}");
			}
			catch (Exception ex)
			{
				MessageBox.Show($"Failed to load settings:\n{_settingsPath}\n\nError: {ex.Message}");
			}
		}

		private void chbxUseLLM_CheckedChanged(object sender, EventArgs e)
		{
			if (chbxUseLLM.Checked)
			{
				panelLLM.Enabled = true;
				panelLLM.Visible = true;
				radioURL.Checked = true;
                panelURL.Visible = true;
			}
			else
			{
				panelLLM.Enabled = false;
				panelLLM.Visible = false;
                panelPrompt.Enabled = false;
                panelPrompt.Visible = false;
                panelURL.Enabled = false;
                panelURL.Visible = false;
            }
		}

		private void radioURL_CheckedChanged(object sender, EventArgs e)
		{
			if (radioURL.Checked)
			{
				loadUrl();
				panelURL.Enabled = true;
				panelURL.Visible = true;
				panelURL.BringToFront();
				panelPrompt.Enabled = false;
				panelPrompt.Visible = false;
			}
		}

		private void radioPrompt_CheckedChanged(object sender, EventArgs e)
		{
			if (radioPrompt.Checked)
			{	
				loadPrompt();
				panelPrompt.Enabled = true;
				panelPrompt.Visible = true;
				panelPrompt.BringToFront();
				panelURL.Enabled = false;
				panelURL.Visible = false;
			}
		}

		private void btnSaveSettings_Click(object sender, EventArgs e)
		{
            saveSettings();
		}

		private void saveSettings()
		{
            string url = txtURL.Text.Trim();
            string prompt = richTextPrompt.Text.Trim();

            if (!string.IsNullOrEmpty(url) && !looksLikeUrl(url))
            {
                MessageBox.Show("Please enter a valid URL format (e.g., http://example.com) or leave empty.");
                return;
            }

            var updater = new settingsFileUpdater(_settingsPath, _promptPath);
            if (panelURL.Enabled)
            {
                updater.updateUrlDelphi(url);
            }
            if (panelPrompt.Enabled)
            {
                updater.updatePromptDelphi(prompt);
            }
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

        private void btnReturn_Click(object sender, EventArgs e)
        {
            this.Hide();
            var form = new formMain();
            form.ShowDialog();
            this.Close();
        }

        private void loadUrl()
        {
            try
            {
                _settingsParser.LoadUrlFileDelphi(_settingsPath);
                txtURL.Text = _settingsParser.Url;

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

        private void loadPrompt()
        {
            try
            {
                _settingsParser.LoadPromptFileDelphi(_promptPath);
				richTextPrompt.Text = _settingsParser.Prompt;
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

        private void btnCreateTestUsers_Click(object sender, EventArgs e)
        {
            var runner = new scriptRunner(pythonProjectPath); 
            string scriptPath;

            try
            {
                if (!chbxUseLLM.Checked)
                {
                   
                    scriptPath = @"TestDataProject\scripts(Generic)\train_ctgan.py";
                    runner.runScripts(pythonProjectPath, scriptPath);
                }
                else
                {
                    if (radioURL.Checked)
                    {
                        saveSettings(); 
                        scriptPath = @"TestDataPtoject\web_input_module\run_url_pipeline.py";
                        runner.runScripts(pythonProjectPath, scriptPath);
                    }
                    else if (radioPrompt.Checked)
                    {
                        string prompt = richTextPrompt.Text.Trim();
                        saveSettings();
                        scriptPath = @"TestDataProject\generated_mode\run_all.py";
                        DialogResult result = MessageBox.Show(
                              $"You are now running a prompt-based code.\n\nPlease confirm your prompt:\n\n{prompt}\n\nDo you want to proceed?",
                              "Confirm Prompt",
                              MessageBoxButtons.YesNo,
                              MessageBoxIcon.Question,
                              MessageBoxDefaultButton.Button2
                        );

                        if (result == DialogResult.Yes)
                        {
                            runner.runScripts(pythonProjectPath, scriptPath);
                        }
                        else
                        {
                            MessageBox.Show("Prompt execution was cancelled.");
                        }
                    }
                    else
                    {
                        MessageBox.Show("Please select either URL or Prompt option.", "Selection Required", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Script execution failed:\n{ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            this.Hide();
            var form3 = new formTestCase();
            form3.ShowDialog();
            this.Close();
        }
    }
}
