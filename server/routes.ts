import type { Express } from "express";
import type { Server } from "http";
import { storage } from "./storage";
import { api } from "@shared/routes";
import { z } from "zod";
import { UwmClient } from "./uwm";
import { SshTunnel } from "./tunnel";
import fs from "fs";
import path from "path";

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {

  // Setup SSH Key
  const keyPath = path.join(process.cwd(), "server", "key.pem");
  // Copy the key from attached_assets if it doesn't exist in server/
  const sourceKeyPath = path.join(process.cwd(), "attached_assets", "valargen-staging_key_1771049939904.pem");
  
  if (fs.existsSync(sourceKeyPath)) {
     const keyContent = fs.readFileSync(sourceKeyPath, 'utf-8');
     fs.writeFileSync(keyPath, keyContent, { mode: 0o600 }); // Secure permissions
  }

  // Initialize Tunnel and Client
  const tunnel = new SshTunnel({
    host: "4.227.184.143",
    username: "vg-stg-user",
    privateKeyPath: keyPath,
    localPort: 1080
  });

  // Start tunnel on server start (non-blocking)
  tunnel.start().catch(err => console.error("Failed to start SSH tunnel:", err));

  const uwmClient = new UwmClient();

  app.post(api.quote.get.path, async (req, res) => {
    try {
      const input = api.quote.get.input.parse(req.body);
      
      // Log the request (fire and forget)
      storage.logQuoteRequest(input);

      // Ensure tunnel is ready or try to restart? 
      // For now, we assume it's running. The UwmClient handles the proxy connection.
      
      const response = await uwmClient.getQuote(input);
      res.json(response);

    } catch (err) {
      console.error("Quote API Error:", err);
      if (err instanceof z.ZodError) {
        return res.status(400).json({
          message: "Validation Error",
          details: err.errors
        });
      }
      res.status(500).json({ 
        message: err instanceof Error ? err.message : "Internal Server Error" 
      });
    }
  });

  return httpServer;
}
