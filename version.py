"""
Version Information

Contains application version and build information.
"""

__version__ = "2.1.0"
__build_date__ = "2025-07-28"
__build_number__ = 210

# Version history
VERSION_HISTORY = {
    "2.1.0": {
        "release_date": "2025-07-28",
        "features": [
            "🚀 Removed Fast Mode for rock-solid download stability",
            "🎯 Simplified download process with consistent user-configured timeouts",
            "🗑️ Complete CLI module removal for better maintainability",
            "⚙️ User-configured timeout properly applied to all servers and exchanges",
            "🔧 Improved error handling and retry logic across all downloaders",
            "📊 Simplified configuration with reduced complexity",
            "🛡️ Enhanced reliability with predictable download behavior"
        ],
        "bug_fixes": [
            "Fixed hardcoded timeout issues that bypassed user settings",
            "Resolved server-specific timeout conflicts and inconsistencies",
            "Eliminated CLI navigation and interaction problems",
            "Better memory management during concurrent downloads",
            "Improved download reliability across NSE and BSE exchanges",
            "Fixed fast mode optimizations that caused missed downloads",
            "Resolved complex retry logic that led to unpredictable behavior"
        ]
    },
    "2.0.0": {
        "release_date": "2025-01-23",
        "features": [
            "Added BSE INDEX downloader support",
            "Implemented fast download strategy (5-10x faster)",
            "Added GitHub market holidays integration",
            "Enhanced GUI with dynamic options",
            "Added response timeout configuration",
            "Implemented memory-based file processing",
            "Added update checker system"
        ],
        "bug_fixes": [
            "Fixed application freeze on stop download",
            "Resolved BSE INDEX column ordering issue",
            "Fixed console log clearing after download complete",
            "Improved GUI flickering during downloads"
        ]
    },
    "1.0.0": {
        "release_date": "2024-12-01",
        "features": [
            "Initial release",
            "NSE EQ, FO, SME downloaders",
            "BSE EQ downloader",
            "Basic GUI interface",
            "File management system"
        ]
    }
}

def get_version():
    """Get current version string"""
    return __version__

def get_build_info():
    """Get build information"""
    return {
        "version": __version__,
        "build_date": __build_date__,
        "build_number": __build_number__
    }

def get_version_history():
    """Get version history"""
    return VERSION_HISTORY
