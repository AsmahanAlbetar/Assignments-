library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity TB is
end entity;

architecture arch_TB of TB is

    component doorController is 
         port (
         Clk   :        in std_logic;
         reset :        in std_logic; --Active low asynchronus reset
         sensor_in :    in std_logic; --  1 = open , 0 = close

         door_state_led :  out std_logic_vector(1 downto 0); 
         remaining_time :  out std_logic_vector(1 downto 0)
        ) ;
    end component;

    constant clk_cycle : time := 50 ns;
    signal Clk             : std_logic := '0';
    signal reset           : std_logic := '1';
    signal sensor_in       : std_logic := '0';
    signal door_state_led          : std_logic_vector (1 downto 0) := "00";
    signal remaining_time          : std_logic_vector (1 downto 0) := "00";

    begin
        clk_simulation:
        process
            begin
                loop
                  Clk <= '1';
                  wait for clk_cycle / 2;
                  Clk <= '0';
                  wait for clk_cycle / 2;
                end loop;
        end process;

    DUT : doorController
        port map(
             Clk             => Clk;
             Reset           => reset;
             sensor_in       => sensor_in;       
             door_state_led  => door_state_led;          
             remaining_time  => remaining_time          
        );

    
    process

        variable all_passed : boolean := true;
    begin 
        Reset <= '1';
        wait until rising_edge(Clk);
        -- Reset pulse aligned to clock edges
        Reset <= '0';
        wait until rising_edge(Clk);
        Reset <= '1';
        wait until rising_edge(Clk);

        sensor_in <= '0';

        assert(door_state_led = "00")
            report " failed to stay closed" SEVERITY ERROR

        wait for 200 ns;

        sensor_in <= '1';
         assert(door_state_led = "01")
            report " failed to go to opening" SEVERITY ERROR

        sensor_in <= '0';
        wait for 250 ns
        

        assert(door_state_led = "10" )
            report " failed to go to opened" SEVERITY ERROR
        wait for 500 ns

        assert(door_state_led = "11" )
            report " failed to go to closing" SEVERITY ERROR
        wait for 500 ns

        assert(door_state_led = "11" )
            report " failed to go to closed" SEVERITY ERROR
        wait for 500 ns
        assert FAILED REPORT "Simulation finished successfully." SEVERITY FAILURE
    end process;

end architecture;

