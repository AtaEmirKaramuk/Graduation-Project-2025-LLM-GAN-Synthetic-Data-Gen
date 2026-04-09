using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace FinalProject
{
	internal class scriptRunner
	{
		private readonly string _projectDirectory;
		private readonly settingsFileUpdater _settingsUpdater;
        string pythonProjectPath;

        public scriptRunner(string projectDirectory)
		{
			_projectDirectory = projectDirectory;
		}	

		public async Task runScripts(string pyhtonProjectPath, string scriptPath)
		{
			
			string scriptFullPath = Path.Combine(pyhtonProjectPath, scriptPath); 
			string scriptWorkingDirectory = Path.GetDirectoryName(scriptFullPath);
            LoaderForm loader = null;

            try
			{
				if (!File.Exists(scriptFullPath))
				{
					throw new FileNotFoundException($"Python script not found: {scriptFullPath}");
				}

				
				MessageBox.Show($"Executing script at: \"{scriptFullPath}\"");

                loader = new LoaderForm();
                loader.Show();
                loader.Refresh();

                await Task.Run(() =>
                {
                    var psi = new ProcessStartInfo
                    {
                        FileName = Path.Combine(pyhtonProjectPath, ".venv", "Scripts", "python.exe"),
                        Arguments = $"\"{scriptFullPath}\"",
                        WorkingDirectory = Path.Combine(scriptWorkingDirectory),
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        CreateNoWindow = true
                    };

                    psi.EnvironmentVariables["PYTHONPATH"] =
                        Path.Combine(pyhtonProjectPath, "TestCaseGenerator") +
                        ";" +
                        pyhtonProjectPath + ";" + Path.Combine(pyhtonProjectPath, "TestDataProject");

                    using (var process = new Process())
                    {
                        process.StartInfo = psi;
                        process.Start();

                        string output = process.StandardOutput.ReadToEnd();
                        string errors = process.StandardError.ReadToEnd();


                        process.WaitForExit();

                        MessageBox.Show(output + Environment.NewLine + errors);
                    }
                });
			}
			catch (Exception ex)
			{
				throw new ApplicationException($"Execution failed: {ex.Message}", ex);
			}
            finally
            {
                if (loader != null && !loader.IsDisposed)
                {
                    loader.Close();
                    loader.Dispose();
                }
            }
		}
	}
}
