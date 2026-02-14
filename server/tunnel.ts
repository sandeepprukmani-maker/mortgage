import { spawn, type ChildProcess } from "child_process";
import net from "net";

interface TunnelConfig {
  host: string;
  username: string;
  privateKeyPath: string;
  localPort: number;
}

export class SshTunnel {
  private process: ChildProcess | null = null;
  private config: TunnelConfig;
  private isRunning: boolean = false;

  constructor(config: TunnelConfig) {
    this.config = config;
  }

  async start(): Promise<void> {
    if (this.isRunning) {
      console.log("SSH Tunnel already running.");
      return;
    }

    console.log(`Starting SSH Tunnel to ${this.config.username}@${this.config.host} on port ${this.config.localPort}...`);

    // ssh -i key.pem -N -D 1080 -o StrictHostKeyChecking=no user@host
    const args = [
      "-i", this.config.privateKeyPath,
      "-N", // Do not execute a remote command
      "-D", this.config.localPort.toString(), // Dynamic application-level port forwarding (SOCKS)
      "-o", "StrictHostKeyChecking=no", // Avoid interactive prompt
      "-o", "UserKnownHostsFile=/dev/null",
      `${this.config.username}@${this.config.host}`
    ];

    this.process = spawn("ssh", args);

    this.process.stdout?.on("data", (data) => {
      console.log(`[SSH Tunnel] ${data}`);
    });

    this.process.stderr?.on("data", (data) => {
      // SSH usually outputs to stderr for info messages too
      console.log(`[SSH Tunnel Info] ${data}`);
    });

    this.process.on("close", (code) => {
      console.log(`SSH Tunnel exited with code ${code}`);
      this.isRunning = false;
      this.process = null;
      // Optional: Auto-restart logic could go here
    });

    this.isRunning = true;
    
    // Give it a moment to establish
    await new Promise(resolve => setTimeout(resolve, 3000));
    console.log("SSH Tunnel started.");
  }

  stop() {
    if (this.process) {
      this.process.kill();
      this.process = null;
      this.isRunning = false;
    }
  }
}
