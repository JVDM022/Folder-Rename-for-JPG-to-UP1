#include <iostream>
#include <filesystem>
#include <regex>
#include <map>
#include <vector>
#include <algorithm>
#include <fstream>


namespace fs = std::filesystem;

void renameANDCopyFiles(const std::string& srcFolder, const std::string& dstFolder, const std::string& prefix)
{
    if(!fs::exists(srcFolder))
    {
        std::cout << "Source folder does not exist!" << std::endl;
        return;
    }
    if(!fs::exists(dstFolder))
    {
        fs::create_directories(dstFolder);
    }

    std::regex pattern (prefix + R"(_x(\d+)y(\d+)"); // pattern to match the filenames
    std::map<int,int> x_map;
    int x_counter = 0;
    int y_counter =0;
    int prev_x_val = -1;

    for (const auto& entry : fs::directory_iterator(srcFolder)) // iterate through all files in the folder
    {
        std::string filename = entry.path().filename().string();
        std::smatch match;
        if (std::regex_search(filename, match, pattern))
        {
            int x_val = std::stoi(match[1].str());
            int y_val = std::stoi(match[2].str());

            if (x_map.find(x_val) == x_map.end())
            {
                x_map[x_val] = x_counter++; // assign new x_val to x_counter
                y_counter = 0; // reset y_counter
            }
            int new_x = x_map[x_val];
            int new_y = y_counter++;

            std::string extension = entry.path().extension().string();
            std::string new_filename = "x" + std::to_string(new_x) + "y" + std::to_string(new_y) + extension;

            fs::copy(entry.path(), fs::path(dstFolder) / new_filename, fs::copy_options::overwrite_existing);
            std::cout << "Copied and Renamed " << filename << " -> " << new_filename << std::endl;
        }
    }
    std::cout << "Done!" << std::endl;
}

int main()
{
    std::string srcFolder, desFolder, prefix;
    std::cout << "Enter the source folder path: ";
    std::getline(std::cin, srcFolder);
    std::cout << "Enter the source folder path: ";
    std::getline(std::cin, srcFolder);
    std::cout << "Enter the source folder path: ";
    std::getline(std::cin, srcFolder);

    renameANDCopyFiles(srcFolder, desFolder, prefix);
    return 0;
}