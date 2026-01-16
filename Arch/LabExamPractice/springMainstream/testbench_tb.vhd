library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tb_trafficLight is
    port (
        dummy : in std_logic := '0'
    );
end entity;

architecture arch_tb of tb_trafficLight is

    --------------------------------------------------------------------
    -- Component Declaration
    --------------------------------------------------------------------
    component trafficLightController is
        port (
            Clk   : in std_logic;
            reset : in std_logic;
            en    : in std_logic;

            Green  : out std_logic;
            Yellow : out std_logic;
            Red    : out std_logic
        );
    end component;

    --------------------------------------------------------------------
    -- 50 MHz Clock (Period = 20 ns)
    --------------------------------------------------------------------
    constant clk_cycle : time := 20 ns;

    signal Clk     : std_logic := '0';
    signal reset   : std_logic := '0';
    signal en      : std_logic := '1';

    signal Green  : std_logic;
    signal Yellow : std_logic;
    signal Red    : std_logic;

begin

    --------------------------------------------------------------------
    -- Clock Generation (50 MHz)
    --------------------------------------------------------------------
    clk_process :
    process
    begin
        Clk <= '1';
        wait for clk_cycle/2;      -- 10 ns
        Clk <= '0';
        wait for clk_cycle/2;      -- 10 ns
    end process;

    --------------------------------------------------------------------
    -- Instantiate the DUT
    --------------------------------------------------------------------
    DUT : trafficLightController
        port map (
            Clk    => Clk,
            reset  => reset,
            en     => en,
            Green  => Green,
            Yellow => Yellow,
            Red    => Red
        );

    --------------------------------------------------------------------
    -- MAIN SELF-CHECKING TEST
    --------------------------------------------------------------------
    mainProcess :
    process
    begin
        
        ----------------------------------------------------------------
        -- Apply Reset
        ----------------------------------------------------------------
        reset <= '1';
        wait for 5 * clk_cycle;
        reset <= '0';
        wait for 5 * clk_cycle;

        ----------------------------------------------------------------
        -- GREEN SHOULD BE ACTIVE FOR 10 CYCLES
        ----------------------------------------------------------------
        assert (Green = '1' and Yellow = '0' and Red = '0')
            report "ERROR: Expected GREEN state at start"
            severity error;

        wait for 10 * clk_cycle;

        ----------------------------------------------------------------
        -- YELLOW SHOULD BE ACTIVE FOR 5 CYCLES
        ----------------------------------------------------------------
        assert (Green = '0' and Yellow = '1' and Red = '0')
            report "ERROR: Expected YELLOW state after GREEN"
            severity error;

        wait for 5 * clk_cycle;

        ----------------------------------------------------------------
        -- RED SHOULD BE ACTIVE FOR 10 CYCLES
        ----------------------------------------------------------------
        assert (Green = '0' and Yellow = '0' and Red = '1')
            report "ERROR: Expected RED state after YELLOW"
            severity error;

        wait for 10 * clk_cycle;

        ----------------------------------------------------------------
        -- FINISH
        ----------------------------------------------------------------
        report "TEST PASSED: Traffic Light Controller works correctly!"
            severity note;

        wait;
    end process;

end architecture;
