import { makeWASocket, useMultiFileAuthState, fetchLatestBaileysVersion } from '@whiskeysockets/baileys';
import qrcode from 'qrcode-terminal';
import { exec } from 'child_process';
import fs from 'fs';

// Main listener function
async function startListener() {
  const { state, saveCreds } = await useMultiFileAuthState('auth_info_listener');
  const { version } = await fetchLatestBaileysVersion();

  // Load allowed group IDs from messages.json
  const groupData = JSON.parse(fs.readFileSync('./messages.json', 'utf-8'));
  console.log('✅ Authorized group access loaded.');

  const sock = makeWASocket({
    version,
    auth: state,
  });

  sock.ev.on('creds.update', saveCreds);

  sock.ev.on('connection.update', (update) => {
    const { connection, qr } = update;

    if (qr) {
      console.log('📲 Scan the QR code to log in:');
      qrcode.generate(qr, { small: true });
    }

    if (connection === 'close') {
      console.log('🔄 Connection closed. Reconnecting...');
      startListener(); // Restart listener
    } else if (connection === 'open') {
      console.log('✅ Bot is connected and ready!');
    }
  });

  sock.ev.on('messages.upsert', async ({ messages }) => {
    const msg = messages[0];
    if (!msg.message || msg.key.fromMe) return;

    const body = msg.message.conversation || msg.message.extendedTextMessage?.text || '';
    const jid = msg.key.remoteJid;

    if (body.trim() !== "!jobbot") {
      console.log('ℹ️ Non-command message ignored.');
      return;
    }

    const groupAllowed = groupData.find(group => group.groupId === jid);
    if (!groupAllowed) {
      console.log('⛔ Unauthorized group tried to use the command.');
      await sock.sendMessage(jid, { text: "🚫 This group is not allowed to run the job agent." });
      return;
    }

    try {
      const metadata = await sock.groupMetadata(jid);
      const sender = msg.key.participant || msg.key.remoteJid;
      const participant = metadata.participants.find(p => p.id === sender);
      const isAdmin = participant?.admin === 'admin' || participant?.admin === 'superadmin';

      if (!isAdmin) {
        console.log('⛔ Unauthorized user tried to run the job agent.');
        await sock.sendMessage(jid, { text: "🚫 Only group admins can run the job agent." });
        return;
      }

      console.log('✅ Authorized command received. Running job agent...');
      exec("python main.py run", async (error, stdout, stderr) => {
        if (error) {
          console.error('❌ Job agent error:', stderr);
          await sock.sendMessage(jid, { text: "⚠️ Failed to run the job agent." });
        } else {
          console.log('✅ Job agent executed successfully.');
          await sock.sendMessage(jid, { text: "✅ Job agent completed successfully." });
        }
      });
    } catch (err) {
      console.error("❌ Error while processing command:", err);
      await sock.sendMessage(jid, { text: "⚠️ An unexpected error occurred while handling the command." });
    }
  });
}

startListener();
