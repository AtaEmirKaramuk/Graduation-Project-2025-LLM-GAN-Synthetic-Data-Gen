using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Policy;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace FinalProject
{

	public class settingsFileUpdater
	{
		public string FilePath { get; }
		public string PromptPath { get; }
		public bool isInitialized { get; private set; }

		public settingsFileUpdater(string filePath, string promptPath)
		{
			try
			{
				if (string.IsNullOrWhiteSpace(filePath))
					throw new ArgumentNullException(nameof(filePath));

				string fullPath = Path.GetFullPath(filePath);

				string directory = Path.GetDirectoryName(fullPath);
				if (!Directory.Exists(directory))
					throw new DirectoryNotFoundException($"Directory not found: {directory}");

				if (!File.Exists(fullPath))
					throw new FileNotFoundException($"settings.py not found at: {fullPath}");


				FilePath = fullPath;
				PromptPath = promptPath;
				isInitialized = true;
			}
			catch (Exception ex)
			{
				isInitialized = false;
				throw new settingsInitializationException(
					$"Failed to initialize settings updater for path: {filePath}",
					filePath,
					ex);
			}
		}


		public void updateSettingsArgos(bool useGpu, bool useZephyr, bool useDefault, string numZephyrRuns, string url = null)
		{
			try
			{
				var content = new StringBuilder();
				foreach (var line in File.ReadAllLines(FilePath))
				{
					string trimmed = line.Trim();

					if (trimmed.StartsWith("USE_GPU ="))
						content.AppendLine($"USE_GPU = {useGpu.ToString()}");
					else if (trimmed.StartsWith("USE_ZEPHYR ="))
						content.AppendLine($"USE_ZEPHYR = {useZephyr.ToString()}");
					else if (trimmed.StartsWith("ALL_CASES ="))
						content.AppendLine($"ALL_CASES = {useDefault.ToString()}");
					else if (trimmed.StartsWith("NUM_ZEPHYR_RUNS ="))
						content.AppendLine($"NUM_ZEPHYR_RUNS ={numZephyrRuns}");
					else if (url != null && trimmed.StartsWith("URL ="))
						content.AppendLine($"URL = \"{url}\"");
					else
						content.AppendLine(line);
				}

				string backupPath = FilePath + ".bak";
				File.Copy(FilePath, backupPath, overwrite: true);

				try
				{
					File.WriteAllText(FilePath, content.ToString());
				}
				catch
				{
					File.Copy(backupPath, FilePath, overwrite: true);
					throw;
				}
				finally
				{
					if (File.Exists(backupPath))
						File.Delete(backupPath);
				}
			}
			catch (Exception ex)
			{
				throw new ApplicationException($"Failed to update settings in {FilePath}", ex);
			}
		}

		public void updateUrlDelphi(string url)
		{
			var content = new StringBuilder();
			foreach (var line in File.ReadAllLines(FilePath))
			{
				string trimmed = line.Trim();

				if (url != null && trimmed.StartsWith("URL ="))
					content.AppendLine($"URL = \"{url}\"");
			}
		}

        public void updatePromptDelphi(string prompt)
        {
            var content = new StringBuilder();
         
            foreach (var line in File.ReadAllLines(PromptPath))
            {
                string trimmed = line.Trim();

                if (trimmed.StartsWith("\"prompt\":"))
                {
                    content.AppendLine($"  \"prompt\": \"{prompt}\"");
                }
                else
                {
                    content.AppendLine(line);
                }
            }

            File.WriteAllText(PromptPath, content.ToString());
        }
    }


	public class settingsInitializationException : Exception
	{
		public string FilePath { get; }

		public settingsInitializationException(string message, string filePath, Exception innerException)
			: base(message, innerException)
		{
			FilePath = filePath;
		}
	}
}
