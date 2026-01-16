library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity trafficLightController is

    port (
        -- Inputs
        Clk   : in std_logic;
        reset : in std_logic;
        en    : in std_logic;

        -- Outputs
        Green  : out std_logic;
        Yellow : out std_logic;
        Red    : out std_logic
    );

end entity;

architecture arch_trafficLight of trafficLightController is

    -- Define states
    type state is (sGreen, sYellow, sRed);

begin

    process(Clk, reset)
        variable greenCounter  : integer := 0;  -- 10 cycles
        variable yellowCounter : integer := 0;  -- 5 cycles
        variable redCounter    : integer := 0;  -- 10 cycles
        variable myState       : state := sGreen;
    begin

        if reset = '1' then
            -- Reset everything
            greenCounter  := 0;
            yellowCounter := 0;
            redCounter    := 0;
            myState       := sGreen;

            Green  <= '0';
            Yellow <= '0';
            Red    <= '0';

        elsif rising_edge(Clk) and en = '1' then

            case myState is

                ----------------------------------------------------
                -- GREEN
                ----------------------------------------------------
                when sGreen =>
                    if greenCounter < 9 then
                        greenCounter := greenCounter + 1;

                        Green  <= '1';
                        Yellow <= '0';
                        Red    <= '0';
                    else
                        greenCounter := 0;
                        myState := sYellow;
                    end if;

                ----------------------------------------------------
                -- YELLOW
                ----------------------------------------------------
                when sYellow =>
                    if yellowCounter < 4 then
                        yellowCounter := yellowCounter + 1;

                        Green  <= '0';
                        Yellow <= '1';
                        Red    <= '0';
                    else
                        yellowCounter := 0;
                        myState := sRed;
                    end if;

                ----------------------------------------------------
                -- RED
                ----------------------------------------------------
                when sRed =>
                    if redCounter < 9 then
                        redCounter := redCounter + 1;

                        Green  <= '0';
                        Yellow <= '0';
                        Red    <= '1';
                    else
                        redCounter := 0;
                        myState := sGreen;
                    end if;

            end case;

        end if;

    end process;

end architecture;
