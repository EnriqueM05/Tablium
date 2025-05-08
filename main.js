const { app, BrowserWindow } = require("electron");
const path = require("path");

// Keep a global reference of the window object to prevent it from being garbage collected
let mainWindow;

function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 800,
    webPreferences: {
      nodeIntegration: false, // Default is false for security
      contextIsolation: true, // Protect against prototype pollution
      preload: path.join(__dirname, "preload.js"), // Use a preload script
    },
  });

  // Load your HTML file
  mainWindow.loadFile("index.html");

  // Open DevTools in development (optional)
  // mainWindow.webContents.openDevTools()

  // Handle window being closed
  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

// Create window when Electron has finished initialization
app.whenReady().then(createWindow);

// Quit when all windows are closed, except on macOS
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

// On macOS, re-create window when dock icon is clicked
app.on("activate", () => {
  if (mainWindow === null) {
    createWindow();
  }
});
